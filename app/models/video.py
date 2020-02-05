from flask import current_app
from app import db

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
    video_file = db.relationship('VideoFile', backref='video', lazy='dynamic')

    def launch_task(self, name, *args, **kwargs):
        rq_job = current_app.task_queue.enqueue('app.tasks.' + name, *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name, channel_id=self.channel_id, video_id=self.id, kwargs=kwargs)
        db.session.add(task)
        return task

    def __repr__(self):
        return '<Video {}>'.format(self.id)

