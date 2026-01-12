from flask import render_template, abort
from flask_login import login_required, current_user
from app.utils.string_utils import hide_email_util
from app.utils.decorator_utils import auth_required
from app.utils.result_utils import Result, Error, Ok

@auth_required
def account():
    result:Result[str, Exception] = hide_email_util(str(current_user.email))

    if isinstance(result, Error):
        email = "*******@********"
    else:
        email = result.data
    return render_template("account.html", email=email)