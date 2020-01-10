from flask_restful import Api, Resource, abort

from app.api import bp
api = Api(bp)


def get_shows(id=None):
    shows = [
        dict(id=1, name="Dude Perfect", url="https://www.youtube.com/channel/UCRijo3ddMTht_IHyNSNXpNQ"),
        dict(id=2, name="DanTDM", url="https://www.youtube.com/user/TheDiamondMinecart")
    ]
    if id:
        if id == 0:
            abort(400)
        try:
            show = shows[id-1]
        except:
            abort(404, error="Invalid show ID")
        return show
    else:
        return shows

class ShowsAPI(Resource):
    def get(self):
        return {
            'shows': get_shows()
            }

class ShowsIDAPI(Resource):
    def get(self, id):
        return {
            'shows': get_shows(id=id)
            }

api.add_resource(ShowsAPI, '/shows')
api.add_resource(ShowsIDAPI, '/shows/<int:id>')
