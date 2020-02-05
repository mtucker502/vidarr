from flask import Blueprint
from flask_restful import fields

API_VERSION_V1 = 'v1'
API_VERSION = API_VERSION_V1

task_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'kwargs': fields.String,
    'channel_id': fields.String,
    'video_id': fields.String,
    'complete': fields.Boolean,
    '_created': fields.String,
    'uri': fields.Url('api.task')
}

bp = Blueprint('api', __name__)

from app.api import channels, videos, diskspace, tasks