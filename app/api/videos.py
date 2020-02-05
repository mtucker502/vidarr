from flask_restful import Api, Resource, abort, reqparse, fields, marshal
from app import db
from app.models import Video
from app.api import bp
api = Api(bp)

video_fields = {
    'id': fields.Integer,
    'channel_id': fields.String,
    'video_id': fields.String,
    'title': fields.String,
    'duration': fields.String,
    'ydl_options': fields.String,
    'monitor': fields.Boolean,
    'filename': fields.String,
    'exists': fields.Boolean,
    'uri': fields.Url('api.video')
}

def get_videos(id=None):
    if id:
        video = Video.query.get(id)
        
        if video is not None:
            return marshal(video, video_fields)
        else:
            abort(404, error="Invalid video ID")

    else:
        videos = Video.query.all()
        return [marshal(video, video_fields) for video in videos]

class VideoListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, required = True,
            help = 'No video name provided', location = 'json')
        self.reqparse.add_argument('url', type = str, required = True,
            help = 'No video url provided', location = 'json')
        self.reqparse.add_argument('ydl_options', type = str, default = "", location = 'json')
        self.reqparse.add_argument('monitor', type = bool, default = True, location = 'json')
        self.reqparse.add_argument('file', type = str, required = True, location = 'json')
        super(VideoListAPI, self).__init__()

    def get(self):
        return {
            'videos': get_videos()
            }
    
    def post(self):
        args = self.reqparse.parse_args()

        video = Video(
            name = args['name'],
            url = args['url'],
            ydl_options = args['ydl_options'],
            monitor = args['monitor'],
            folder = args['folder']
        )

        db.session.add(video)
        db.session.commit()

        return {'video': marshal(video, video_fields)}, 201

class VideoAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'json')
        self.reqparse.add_argument('url', type = str, location = 'json')
        self.reqparse.add_argument('ydl_options', type = str, location = 'json')
        self.reqparse.add_argument('monitor', type = bool, location = 'json')
        self.reqparse.add_argument('folder', type = str, location = 'json')
        super(VideoAPI, self).__init__()

    def get(self, id):
        return {
            'video': get_videos(id=id)
            }

    def put(self, id):
        video = Video.query.get(id)

        if video is not None:
            args = self.reqparse.parse_args()
            for k, v in args.items():
                if v is not None:
                    setattr(video, k, v)
            db.session.commit()
            return {'video': get_videos(id=id)}
        else:
            abort(404, error="Invalid video ID")
        
    def delete(self, id):
        video = Video.query.get(id)
        if video is not None:
            db.session.delete(video)
            db.session.commit()
            return {'result': True}, 204
        else:
            abort(404, error="Invalid video ID")


api.add_resource(VideoListAPI, '/videos')
api.add_resource(VideoAPI, '/videos/<int:id>', endpoint='video')
