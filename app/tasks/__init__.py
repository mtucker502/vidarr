from redis import Redis
import rq
from flask import current_app
from app import create_app, db
from app.models import Channel, Video, Task
from datetime import datetime
from flask_restful import abort
import youtube_dl

_CHANNEL_TASKS = ['RefreshChannel']
_VIDEO_TASKS = []
_TASKS = _CHANNEL_TASKS + _VIDEO_TASKS

def _set_task_progress(progress, filename=None):
    job = rq.get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        if progress >= 100:
            task.complete = True
            if filename:
                task.report = filename
        db.session.commit()

def launch_task(name, *args, **kwargs):
    if name not in _TASKS:
        abort(400, error='Invalid task name')
    
    # Video specific tasks
    if "video_id" in kwargs and name in _VIDEO_TASKS:
        video = Video.query.get_or_404(kwargs["video_id"])
        task = video.launch_task(name, **kwargs)
        return task
    
    # Channel specific tasks
    if "channel_id" in kwargs and name in _CHANNEL_TASKS:
        channel = Channel.query.get_or_404(kwargs["channel_id"])
        task = channel.launch_task(name, **kwargs)
        return task

    # Non Specific task
    rq_job = current_app.task_queue.enqueue('app.tasks.' + name, *args, **kwargs)
    task = Task(id=rq_job.get_id(), name=name, kwargs=kwargs)
    db.session.add(task)
    return task

def RefreshChannel(id=None, **kwargs):
    print("Channel refresh process started!!!")
    job = rq.get_current_job()
    task = Task.query.get(job.get_id())
    if task.channel:
        channels = [task.channel]
    else:
        channels = Channel.query.all()
        if not channels:
            # no channels, no work
            _set_task_progress(100)
            return True

    for channel in channels:
        with youtube_dl.YoutubeDL() as ydl:
            video_list = ydl.extract_info(channel.url, download=False)['entries']
            for entry in video_list:

                if channel.videos.filter_by(video_id=entry['id']).first():
                    print('Video (id {}) already exists. Skipping...'.format(entry['id']))
                    continue # exit current for loop. TODO: Should we just update the object instead?

                video = Video(
                    title=entry['title'],
                    channel_id = task.channel_id,
                    video_id = entry['id'],
                    duration=entry['duration'],
                    # upload_date=entry['upload_date'], #TODO need to convert to datetime object first
                    monitor=channel.monitor
                    )
                
                print('Video (id {}) added.'.format(entry['id']))
                db.session.add(video)
    
    db.session.commit()
    _set_task_progress(100)

# must stay at bottom to prevent circular imports
app = create_app()
app.app_context().push()