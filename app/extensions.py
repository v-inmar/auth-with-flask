from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

# Set the login view for Flask-Login
login_manager.login_view = 'auth_bp.login' # This tells login manager where to redirect if login is required
login_manager.login_message_category = 'danger' # Category for flash messages