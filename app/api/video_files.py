from flask_restful import Resource, abort, reqparse, fields, marshal
from app import db
from app.models import VideoFile

video_file_fields = {
    'id': fields.Integer,
    'path': fields.String,
    'size': fields.String,
    'format': fields.String,
    'channel_id': fields.String,
    'video__id': fields.String,
    'uri': fields.Url('api.video_file')
}

def get_video_files(id=None):
    if id:
        video_file = VideoFile.query.get(id)
        
        if video_file is not None:
            return marshal(video_file, video_file_fields)
        else:
            abort(404, error="Invalid video_file ID")

    else:
        video_files = VideoFile.query.all()
        return [marshal(video_file, video_file_fields) for video_file in video_files]

class VideoFileListAPI(Resource):
    def get(self):
        return {
            'video_files': get_video_files()
            }

class VideoFileAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'json')
        self.reqparse.add_argument('url', type = str, location = 'json')
        self.reqparse.add_argument('ydl_options', type = str, location = 'json')
        self.reqparse.add_argument('monitor', type = bool, location = 'json')
        self.reqparse.add_argument('folder', type = str, location = 'json')
        super(video_fileAPI, self).__init__()

    def get(self, id):
        return {
            'video_file': get_video_files(id=id)
            }

    def put(self, id):
        video_file = VideoFile.query.get(id)

        if video_file is not None:
            args = self.reqparse.parse_args()
            for k, v in args.items():
                if v is not None:
                    setattr(video_file, k, v)
            db.session.commit()
            return {'video_file': get_video_files(id=id)}
        else:
            abort(404, error="Invalid video_file ID")
        
    def delete(self, id):
        video_file = VideoFile.query.get(id)
        if video_file is not None:
            #TODO delete video file via OS
            db.session.delete(video_file)
            db.session.commit()
            return {'result': True}, 204
        else:
            abort(404, error="Invalid video_file ID")
