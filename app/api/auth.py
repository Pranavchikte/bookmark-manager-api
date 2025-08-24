from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from ..models import User
import mongoengine.errors as errors
from ..extensions import bcrypt


auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POSt'])
def register():
    body = request.get_json()
    if not body or not body.get('email') or not body.get('password'):
        return jsonify({"error": "Email and password are required"}), 400
    
    email = body.get('email')
    password = body.get('password')
    
    try: 
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = User(email=email, password=hashed_password)
        
        new_user.save()
        
        return jsonify({'msg': "User created successfully."}), 201
    
    except errors.NotUniqueError:
        return jsonify({"error": "Email already exists"}),409
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@auth_bp.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    if not body or not body.get('email') or not body.get('password'):
        return jsonify({"error": "Email and Password are required"}), 400
    
    email = body.get('email')
    password = body.get('password')
    
    try:
        
        user = User.objects(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200
        
        else:
            return jsonify({"error": "Invalid email or password"}), 401
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200