from flask_restful import Api, Resource, abort
from app.utils import dict_helper
from app.models import Channel
from app.api import bp
api = Api(bp)

def get_channels(id=None):
    columns = Channel.__table__.columns.keys()

    if id:
        channel = Channel.query.filter_by(id=id).first()
        
        if channel is not None:
            return dict_helper(channel, columns)
        else:
            abort(404, error="Invalid channel ID")

    else:
        channels = Channel.query.all()
        return [dict_helper(channel, columns) for channel in channels]

class ChannelsAPI(Resource):
    def get(self):
        return {
            'channels': get_channels()
            }

class ChannelAPI(Resource):
    def get(self, id):
        return {
            'channel': get_channels(id=id)
            }

api.add_resource(ChannelsAPI, '/channels')
api.add_resource(ChannelAPI, '/channels/<int:id>')
