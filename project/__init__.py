import os
from flask_celeryext import FlaskCeleryExt
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from project.config import config 
from project.celery_utils import make_celery
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)


# Configuration


def create_app(config_name=None):
    
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    app.config['SECRET_KEY'] = 'your_strong_secret_key'
    app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    
    db.init_app(app)       
    migrate.init_app(app,db)
    ext_celery.init_app(app)
    jwt = JWTManager(app)
   
     # register blueprints
    from project.users import users_blueprint
    app.register_blueprint(users_blueprint)
    
    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}
    return app

