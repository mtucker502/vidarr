from flask_restful import Api, Resource, abort
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

class VideosAPI(Resource):
    def get(self):
        return {
            'videos': get_videos()
            }

class VideoAPI(Resource):
    def get(self, id):
        return {
            'video': get_videos(id=id)
            }

api.add_resource(VideosAPI, '/videos')
api.add_resource(VideoAPI, '/videos/<int:id>')
