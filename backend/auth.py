import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from models import User, db

class JWTManager:
    @staticmethod
    def generate_token(user_id, expires_in=86400):
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return token
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token and return user_id"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload.get('user_id')
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def token_required(f):
        """Decorator for protected routes"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    return jsonify({'message': 'Invalid token format'}), 401
            
            if not token:
                return jsonify({'message': 'Token is missing'}), 401
            
            user_id = JWTManager.verify_token(token)
            if user_id is None:
                return jsonify({'message': 'Token is invalid or expired'}), 401
            
            user = User.query.get(user_id)
            if user is None:
                return jsonify({'message': 'User not found'}), 401
            
            return f(user, *args, **kwargs)
        return decorated

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        """Register a new user"""
        if User.query.filter_by(username=username).first():
            return None, 'Username already exists'
        
        if User.query.filter_by(email=email).first():
            return None, 'Email already exists'
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user, None
    
    @staticmethod
    def login_user(username, password):
        """Login user and return token"""
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            return None, 'Invalid username or password'
        
        token = JWTManager.generate_token(user.id)
        return token, None
    
    @staticmethod
    def refresh_token(token):
        """Refresh JWT token"""
        user_id = JWTManager.verify_token(token)
        if user_id is None:
            return None, 'Token is invalid or expired'
        
        new_token = JWTManager.generate_token(user_id)
        return new_token, None
