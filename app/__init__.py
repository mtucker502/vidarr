from flask import Flask
import flask_restful
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
import rq
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api import bp as api_v1_bp
    from app.api import API_VERSION_V1
    app.register_blueprint(api_v1_bp, 
                        url_prefix='/{prefix}/{version}'.format(
                            prefix='api', version=API_VERSION_V1)
                        )

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue(app.config['REDIS_QUEUE'], connection=app.redis)


    return app

from app import models