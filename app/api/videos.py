from flask_restful import Api, Resource, abort, reqparse
from app.utils import dict_helper
from app.models import Video
from app.api import bp
api = Api(bp)

def get_videos(id=None):
    columns = Video.__table__.columns.keys()

    if id:
        video = Video.query.filter_by(id=id).first()
        
        if video is not None:
            return dict_helper(video, columns)
        else:
            abort(404, error="Invalid video ID")

    else:
        videos = Video.query.all()
        return [dict_helper(video, columns) for video in videos]

class VideoListAPI(Resource):
    def get(self):
        return {
            'videos': get_videos()
            }
    
    def post(self):
        pass

class VideoAPI(Resource):
    def get(self, id):
        return {
            'video': get_videos(id=id)
            }
    
    def put(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(VideoListAPI, '/videos')
api.add_resource(VideoAPI, '/videos/<int:id>', endpoint='video')
