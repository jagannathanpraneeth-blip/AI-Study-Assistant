from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    materials = db.relationship('Material', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    progress = db.relationship('Progress', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Material(db.Model):
    __tablename__ = 'materials'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)
    file_size = db.Column(db.Integer)
    pages = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    quizzes = db.relationship('Quiz', backref='material', lazy='dynamic', cascade='all, delete-orphan')
    progress = db.relationship('Progress', backref='material', lazy='dynamic', cascade='all, delete-orphan')

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    material_id = db.Column(db.String(36), db.ForeignKey('materials.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    questions = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    submissions = db.relationship('Submission', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')

class Progress(db.Model):
    __tablename__ = 'progress'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    material_id = db.Column(db.String(36), db.ForeignKey('materials.id'), nullable=False)
    pages_read = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Integer, default=0)
    completion_percentage = db.Column(db.Float, default=0.0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Submission(db.Model):
    __tablename__ = 'submissions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_id = db.Column(db.String(36), db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    answers = db.Column(db.JSON, nullable=False)
    score = db.Column(db.Float)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
