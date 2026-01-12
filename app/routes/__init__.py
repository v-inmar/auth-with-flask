from flask import Blueprint

auth_bp = Blueprint(name="auth_bp", import_name=__name__, template_folder="templates", url_prefix="/auth")
from app.routes.auth import signup, login, logout

# login - /auth/login
auth_bp.add_url_rule(
    rule="/login",
    endpoint="login",
    view_func=login,
    methods=["GET", "POST"]
)

# signup - /auth/signup
auth_bp.add_url_rule(
    rule="/signup",
    endpoint="signup",
    view_func=signup,
    methods=["GET", "POST"]
)

# signup - /auth/logout
auth_bp.add_url_rule(
    rule="/logout",
    endpoint="logout",
    view_func=logout,
    methods=["GET"]
)


home_bp = Blueprint(name="home_bp", import_name=__name__, template_folder="templates")
from app.routes.home import home

# home - /
home_bp.add_url_rule(
    rule="/",
    endpoint="home",
    view_func=home,
    methods=["GET"]
)

# home - /home
home_bp.add_url_rule(
    rule="/home",
    endpoint="home",
    view_func=home,
    methods=["GET"]
)

# home - /index
home_bp.add_url_rule(
    rule="/index",
    endpoint="home",
    view_func=home,
    methods=["GET"]
)

account_bp = Blueprint(name="account_bp", import_name=__name__, template_folder="templates", url_prefix="/account")
from app.routes.protected import account

# account - /account
account_bp.add_url_rule(
    rule="",
    endpoint="account",
    view_func=account,
    methods=["GET"]
)


profile_bp = Blueprint(name="profile_bp", import_name=__name__, template_folder="templates", url_prefix="/profile")
from app.routes.profile import profile

# profile - /profile/123abc
profile_bp.add_url_rule(
    rule="/<pid>",
    endpoint="profile",
    view_func=profile,
    methods=["GET"]
)