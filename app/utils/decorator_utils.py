from functools import wraps
from flask_login import login_required, current_user
from flask import redirect, url_for, abort

def auth_not_required(f):
    """
    Decorator that prevents authenticated users from accessing routes meant for unauthenticated users.

    If the current user is already authenticated, they are redirected to the home page.
    Otherwise, the wrapped view function is executed normally.

    Parameters
    ----------
    f : function
        The Flask view function to wrap.

    Returns
    -------
    function
        A wrapper function that either redirects authenticated users or executes the given view.
    """
    wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("home_bp.home"))
        return f(*args, **kwargs)
    return wrapper


def auth_required(f):
    """
    Decorator that ensures only active, authenticated users can access a route.

    This decorator extends Flask-Login’s @login_required by also checking if the user’s account
    has been deactivated or deleted. If so, the user is redirected to the login page.

    Parameters
    ----------
    f : function
        The Flask view function to protect.

    Returns
    -------
    function
        A wrapper function that enforces authentication and user account status checks.
    """
    wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.datetime_deactivated or current_user.datetime_deleted:
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)
    return wrapper
