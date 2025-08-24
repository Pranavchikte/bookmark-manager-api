from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from mongoengine import connect
from flask_jwt_extended import JWTManager
from .extensions import bcrypt
from datetime import timedelta

def create_app(test_config=None): # Accept an optional test_config
    load_dotenv()
    app = Flask(__name__)

    if test_config is None:
        # Load the regular config if not testing
        app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
        # Set a default secret key for tests
        app.config["JWT_SECRET_KEY"] = "my-test-secret"

    CORS(app)
    jwt = JWTManager(app)
    bcrypt.init_app(app)

    mongo_uri = test_config.get('MONGO_URI') if test_config else os.getenv('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI is not set in the environment variables.")
    connect(host=mongo_uri, uuidRepresentation='standard')

    # Import and register Blueprints
    from .api.health import health_bp
    from .api.auth import auth_bp
    from .api.items import items_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(items_bp)

    return app