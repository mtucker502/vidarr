import json
from flask_restful import Resource, abort, reqparse, marshal, fields
from flask import current_app
from app import db
from app.models import Task
from app.tasks import launch_task

task_fields = {
    'id': fields.String,
    'name': fields.String,
    'kwargs': fields.String,
    'channel_id': fields.String,
    'video_id': fields.String,
    'complete': fields.Boolean,
    '_created': fields.String,
    'uri': fields.Url('api.task')
}

def get_tasks(id=None):
    if id:
        task = Task.query.get(id)
        
        if task is not None:
            return marshal(task, task_fields)
        else:
            abort(404, error="Invalid task ID")

    else:
        tasks = Task.query.all()
        return [marshal(task, task_fields) for task in tasks]

class TaskListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, required = True,
            help = 'No task name provided', location = 'json')
        self.reqparse.add_argument('kwargs', type = str, required = False, location = 'json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return {
            'tasks': get_tasks()
            }
    
    def post(self):
        args = self.reqparse.parse_args()

        # convert argparse's string to a dictionary
        if args['kwargs']:
            kwargs = json.loads(args['kwargs'].replace("'", '"'))
        else:
            kwargs = {}
        
        task = launch_task(args['name'], **kwargs)
        db.session.commit()

        return {'task': marshal(task, task_fields)}, 201

class TaskAPI(Resource):
    def get(self, id):
        return {
            'task': get_tasks(id=id)
            }
