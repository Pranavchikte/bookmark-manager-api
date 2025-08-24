from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from mongoengine import connect
from flask_jwt_extended import JWTManager
from .extensions import bcrypt
from datetime import timedelta

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=15)
    CORS(app) 
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)
    
    bcrypt.init_app(app)
    
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI is not set in .env")
    
    connect(host=mongo_uri)
    
    
    from .api.health import health_bp
    from .api.auth import auth_bp
    from .api.items import items_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(items_bp)
        
    return app