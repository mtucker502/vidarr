from flask import abort
import flask_restful

from app.api import bp
api = flask_restful.Api(bp)


def get_shows2(id=None):
    shows2 = [
        dict(id=1, name="Dude Perfect", url="https://www.youtube.com/channel/UCRijo3ddMTht_IHyNSNXpNQ"),
        dict(id=2, name="DanTDM", url="https://www.youtube.com/user/TheDiamondMinecart")
    ]
    if id:
        if id == 0:
            abort(400)
        try:
            show = shows2[id-1]
        except:
            flask_restful.abort(404, error="Invalid show ID")
        return show
    else:
        return shows2

class Shows2API(flask_restful.Resource):
    def get(self):
        return {
            'shows2': get_shows2()
            }

class Show2API(flask_restful.Resource):
    def get(self, id):
        return {
            'shows2': get_shows2(id=id)
            }

api.add_resource(Shows2API, '/shows2')
api.add_resource(Show2API, '/shows2/<int:id>')
