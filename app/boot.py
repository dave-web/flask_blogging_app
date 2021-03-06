
# pylint: disable=import-outside-toplevel
# /app/boot.py
import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


load_dotenv(".env")
DB = SQLAlchemy()


def create_app():
    """Instanciates and configures Flask app.

    :return: configured Flask app
    :rtype: flask.app.Flask
    """
    app = Flask(__name__,
                template_folder=os.path.abspath("app/templates"))

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 90
    app.config["ENV"] = os.getenv("ENV", "dev")
    app.config["FEED_PAGE_SIZE"] = 20

    app.secret_key = os.environ["SECRET_KEY"]
    DB.init_app(app)

    # Needed for Flask-Migrate model changes tracking
    from .models import Like, User, Post  # noqa: F401
    Migrate(app, DB)

    from .blueprints import auth, like, main, post, profile
    app.register_blueprint(auth)
    app.register_blueprint(like)
    app.register_blueprint(main)
    app.register_blueprint(post)
    app.register_blueprint(profile)

    login_manager = LoginManager()
    login_manager.login_view = "main.index"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
