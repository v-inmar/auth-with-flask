from sqlalchemy.exc import SQLAlchemyError
from app.extensions import login_manager
from flask import current_app, Flask

from app.models.user_model import UserModel
from app.models.authid_model import AuthidModel
from app.utils.result_utils import Result, Ok, Error

from flask import render_template
from flask_wtf.csrf import CSRFError
from flask import Flask
from flask import current_app

@login_manager.user_loader
def load_user(authid: str) -> UserModel | None:
    
    model_result: Result[AuthidModel | None, SQLAlchemyError] = AuthidModel.get_by_value(value=authid)
    if isinstance(model_result, Error):
        current_app.logger.error(model_result.error)
        return None
    
    if model_result.data is None:
        return None
    
    authid_model: AuthidModel = model_result.data
    return authid_model.user()
        

def load_blueprints(app: Flask) -> None:
    from app.routes import auth_bp
    from app.routes import home_bp
    from app.routes import account_bp
    from app.routes import profile_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(profile_bp)

    

def load_models() -> None:
    from app.models.user_model import UserModel
    from app.models.authid_model import AuthidModel


def load_error(app: Flask) -> None:

    @app.errorhandler(CSRFError)
    def csrf_error(e) -> str:
        current_app.logger.error(msg=f"{e.description[1]}. Request Header does not contain CSRF Token or has invalid CSRF Token", exc_info=1)
        return render_template("error/csrf_error.html"), 403

    @app.errorhandler(400)
    def bad_request(e) -> str:
        current_app.logger.error(msg=e.description[1], exc_info=1)
        return render_template("error/bad_request.html"), 400

    @app.errorhandler(404)
    def not_found(e) -> str:
        current_app.logger.error(msg=e.description[1], exc_info=1)
        return render_template("error/not_found.html"), 404
    
    @app.errorhandler(500)
    def server_error(e) -> str:
        current_app.logger.error(msg=e.description[1], exc_info=1)
        return render_template("error/server_error.html"), 500
