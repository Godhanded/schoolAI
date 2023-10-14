from schoolAI.config import App_Config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv(".env")


db = SQLAlchemy()

bcrypt = Bcrypt()


def create_app(config_class=App_Config):
    """
    Create a new instance of the app with the given configuration.

    :param config_class: configuration class
    :return: app
    """
    # Initialize Flask-
    app = Flask(__name__)
    app.config.from_object(App_Config)
    # Initialize CORS
    CORS(app, supports_credentials=True)
    # Initialize SQLAlchemy
    db.init_app(app)
    # Initialize Bcrypt
    bcrypt.init_app(app)

    from schoolAI.auth.routes import auth
    from schoolAI.interaction.route import interaction
    from schoolAI.errors.handlers import error

    app.register_blueprint(error)
    app.register_blueprint(auth)
    app.register_blueprint(interaction)

    with app.app_context():
        db.create_all()

    return app
