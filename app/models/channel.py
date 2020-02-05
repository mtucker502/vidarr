from flask import current_app
from app import db

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(120), unique=True)
    ydl_options = db.Column(db.String(128))
    monitor = db.Column(db.Boolean)
    folder = db.Column(db.String(4096), unique=True)
    videos = db.relationship('Video', backref='channel', lazy='dynamic')
    video_files = db.relationship('VideoFile', backref='channel', lazy='dynamic')
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
