# from flask import current_app
from app import db
from datetime import datetime


class BaseModel(object):
    _created = db.Column(db.DateTime, default=datetime.utcnow)
    _modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
