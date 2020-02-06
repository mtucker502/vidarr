from flask_restful import Resource, abort, reqparse, fields, marshal
from app import db
from app.models import Channel

channel_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'url': fields.String,
    'ydl_options': fields.String,
    'monitor': fields.Boolean,
    'folder': fields.String,
    'uri': fields.Url('api.channel')
}

def get_channels(id=None):
    if id:
        channel = Channel.query.get(id)
        
        if channel is not None:
            return marshal(channel, channel_fields)
        else:
            abort(404, error="Invalid channel ID")

    else:
        channels = Channel.query.all()
        return [marshal(channel, channel_fields) for channel in channels]

class ChannelListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, required = True,
            help = 'No channel name provided', location = 'json')
        self.reqparse.add_argument('url', type = str, required = True,
            help = 'No channel url provided', location = 'json')
        self.reqparse.add_argument('ydl_options', type = str, default = "", location = 'json')
        self.reqparse.add_argument('monitor', type = bool, default = True, location = 'json')
        self.reqparse.add_argument('folder', type = str, required = True, location = 'json')
        super(ChannelListAPI, self).__init__()

    def get(self):
        return {
            'channels': get_channels()
            }
    
    def post(self):
        args = self.reqparse.parse_args()

        channel = Channel(
            name = args['name'],
            url = args['url'],
            ydl_options = args['ydl_options'],
            monitor = args['monitor'],
            folder = args['folder']
        )

        db.session.add(channel)
        db.session.commit()

        return {'channel': marshal(channel, channel_fields)}, 201

class ChannelAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'json')
        self.reqparse.add_argument('url', type = str, location = 'json')
        self.reqparse.add_argument('ydl_options', type = str, location = 'json')
        self.reqparse.add_argument('monitor', type = bool, location = 'json')
        self.reqparse.add_argument('folder', type = str, location = 'json')
        super(ChannelAPI, self).__init__()

    def get(self, id):
        return {
            'channel': get_channels(id=id)
            }

    def put(self, id):
        channel = Channel.query.get(id)

        if channel is not None:
            args = self.reqparse.parse_args()
            for k, v in args.items():
                if v is not None:
                    setattr(channel, k, v)
            db.session.commit()
            return {'channel': get_channels(id=id)}
        else:
            abort(404, error="Invalid channel ID")
        
    def delete(self, id):
        channel = Channel.query.get(id)
        if channel is not None:
            db.session.delete(channel)
            db.session.commit()
            #TODO: Cancel all tasks related to channel
            return {'result': True}, 204
        else:
            abort(404, error="Invalid channel ID")
