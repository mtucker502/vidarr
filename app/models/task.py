from app import db
from app.models import BaseModel
from flask import current_app
import redis
import rq

class Task(BaseModel, db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    kwargs = db.Column(db.String(128), index=True)
    complete = db.Column(db.Boolean, default=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100
