from flask import render_template, abort, url_for
from sqlalchemy.exc import SQLAlchemyError
from app.models.user_model import UserModel
from app.utils.result_utils import Result, Ok, Error


def profile(pid) -> str:
    result: Result[UserModel | None, SQLAlchemyError] =UserModel.get_by_pid(pid=pid)
    if isinstance(result, Error):
        abort(500)
    
    if result.data is None:
        abort(404)
    
    user_model: UserModel = result.data
    firstname: str = str(user_model.firstname).title()
    lastname: str = str(user_model.lastname).title()
    url = url_for('profile_bp.profile', pid=str(user_model.pid))

    user = {
        "firstname": firstname,
        "lastname": lastname,
        "url": url
    }

    return render_template("profile.html", user=user)