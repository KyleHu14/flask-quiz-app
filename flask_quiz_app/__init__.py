from flask import Flask

from .extensions import db, login_manager, migrate
from .routes.main_routes import main_routes

def create_app(config_file = 'config.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    # [Database Setup]
    db.init_app(app)
    migrate.init_app(app, db)

    # [Login Setup]
    # login_manager.init_app(app)
    
    # [Blueprint Setup]
    app.register_blueprint(main_routes)

    return app 