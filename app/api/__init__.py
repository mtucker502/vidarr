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


from app.api import bp
from flask_restful import Api
from app.api.channels import ChannelAPI, ChannelListAPI
from app.api.videos import VideoAPI, VideoListAPI
from app.api.video_files import VideoFileAPI, VideoFileListAPI
from app.api.tasks import TaskAPI, TaskListAPI
from app.api.diskspace import DiskSpaceAPI

api = Api(bp)

api.add_resource(ChannelListAPI, '/channels')
api.add_resource(ChannelAPI, '/channels/<int:id>', endpoint='channel')
api.add_resource(VideoListAPI, '/videos')
api.add_resource(VideoAPI, '/videos/<int:id>', endpoint='video')
api.add_resource(VideoFileListAPI, '/video_files')
api.add_resource(VideoFileAPI, '/video_files/<int:id>', endpoint='video_file')
api.add_resource(TaskListAPI, '/tasks')
api.add_resource(TaskAPI, '/tasks/<id>', endpoint='task')
api.add_resource(DiskSpaceAPI, '/diskspace')
