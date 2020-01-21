from flask_restful import Api, Resource, abort, reqparse, fields, marshal
import psutil
from app.api import bp
api = Api(bp)

diskspace_fields = {
    'path': fields.Integer,
    'label': fields.String,
    'freeSpace': fields.String,
    'totalSpace': fields.String
}

def get_diskspace():
    disks = []
    partitions = psutil.disk_partitions(all=True)
    for p in partitions:
        util = psutil.disk_usage(p.mountpoint)
        disks.append(
            dict(
                path=p.mountpoint,
                label=None,
                freeSpace=util.free,
                totalSpace=util.total
            )
        
        )
    
    return disks

class DiskSpaceAPI(Resource):

    def get(self):
        return {
            'disks': get_diskspace()
            }

api.add_resource(DiskSpaceAPI, '/diskspace')
