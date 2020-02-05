from app import db
from app.models import BaseModel

class VideoFile(BaseModel, db.Model):
    id = db.Column(db.String(36), primary_key=True)
    path = db.Column(db.String(4096), unique=True)
    size = db.Column(db.String(128))
    format = db.Column(db.String(32))
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
