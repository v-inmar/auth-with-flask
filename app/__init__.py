import logging, os
from typing import Any, Dict
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from config import Config

from app.extensions import db, login_manager, migrate, csrf
from app.utils.logger_utils import CustomLogFormatter


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True) # changes resolution of filenames
    app.url_map.strict_slashes = False # i.e. /users and /users/ both match without redirects
    app.config.from_object(Config) # loads configuration

    # -- Create logging feature -- #
    # Set the log path
    log_path = "./logs/app.log"

    # Create log formatter
    formatter = CustomLogFormatter("[%(asctime)s] %(levelname)s: %(remote_addr)s %(method)s:%(url)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Create the /log directory (if it doesnt exsit yet)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Create log handler
    handler = TimedRotatingFileHandler(
        filename=log_path,
        utc=True,
        when="midnight"
    )

    # Set log level
    handler.setLevel(logging.INFO) # Set log level
    handler.setFormatter(formatter) # Set the formatter

    app.logger.addHandler(handler) # Add the log handler into the Flask app instance

    # -- End Create logging feature -- #

    db.init_app(app=app)
    login_manager.init_app(app=app)
    migrate.init_app(app=app,db=db)
    csrf.init_app(app=app)




    # load user(for flask-login), blueprints and models
    from app.utils.loader_utils import load_user
    # load_user() does not need to be called, just imported

    from app.utils.loader_utils import load_models, load_blueprints, load_error
    load_models()
    load_blueprints(app=app)
    load_error(app=app)


    # to suppress favicon 404 error for now
    @app.route('/favicon.ico')
    def favicon():
        return '', 204  # No Content response silences the request
    
    # for health check
    @app.route("/health_check")
    def health_check() -> Dict[str, Any]:
        return {"status": "Running", "code": 200}, 200
    
    return app