from flask import Flask
from flask_cors import CORS, cross_origin
import logging


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    
    app.config.from_object('config.Config')

    from .routes import option_chain
    app.register_blueprint(option_chain, url_prefix='/api/')
    CORS(app)

    with app.app_context():
        from . import routes

        return app