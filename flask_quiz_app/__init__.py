from flask import Flask

from .extensions import db, login_manager, migrate
from .models import User
from .routes.main_routes import main_routes
from .routes.auth import auth

def create_app(config_file = 'config.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    # [Database Setup]
    db.init_app(app)
    migrate.init_app(app, db)

    # [Login Setup]
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    # [Blueprint Setup]
    app.register_blueprint(main_routes)
    app.register_blueprint(auth)

    return app 