from datetime import datetime
from hashlib import md5
from time import time
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

    def __repr__(self):
        return '<Channel {})'.format(self.id)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    video_id = db.Column(db.String(11))
    title = db.Column(db.String(1000))
    duration = db.Column(db.Integer)
    published_date = db.Column(db.DateTime, index=True)
    ydl_options = db.Column(db.String(128))
    size  = db.Column(db.String(128))

    def __repr__(self):
        return '<Video {}>'.format(self.id)