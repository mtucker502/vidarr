from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from app import db
from datetime import datetime
import redis
import rq

class BaseModel(object):
    _created = db.Column(db.DateTime, default=datetime.utcnow)
    _modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(120), unique=True)
    ydl_options = db.Column(db.String(128))
    monitor = db.Column(db.Boolean)
    folder = db.Column(db.String(4096), unique=True)
    videos = db.relationship('Video', backref='channel', lazy='dynamic')
    tasks = db.relationship('Task', backref='channel', lazy='dynamic', order_by="desc(Task._created)")
    fn_template = db.Column(db.String(128))

    def launch_task(self, name, *args, **kwargs):
        rq_job = current_app.task_queue.enqueue('app.tasks.' + name, *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name, channel_id=id,
                    channel=self)
        db.session.add(task)
        return task

    def get_tasks_in_progress(self):
        return Task.query.filter_by(channel=self, complete=False).all()

    def __repr__(self):
        return '<Channel {}>'.format(self.id)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    video_id = db.Column(db.String(11))
    title = db.Column(db.String(1000))
    duration = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, index=True)
    monitor = db.Column(db.Boolean)
    ydl_options = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='video', lazy='dynamic', order_by="desc(Task._created)")

    # exists = db.Column(db.Boolean, default=False)

    def launch_task(self, name, *args, **kwargs):
        rq_job = current_app.task_queue.enqueue('app.tasks.' + name, *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name, channel_id=self.channel_id, video_id=self.id, kwargs=kwargs)
        db.session.add(task)
        return task

    def __repr__(self):
        return '<Video {}>'.format(self.id)

class Task(BaseModel, db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    kwargs = db.Column(db.String(128), index=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    complete = db.Column(db.Boolean, default=False)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100

