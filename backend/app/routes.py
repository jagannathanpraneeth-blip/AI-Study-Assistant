from flask import Blueprint, request, jsonify
from auth import JWTManager, AuthService
from models import User, Material, Quiz, Progress
from file_handler import FileHandler
from gemini_service import GeminiService
from werkzeug.exceptions import BadRequest

api = Blueprint('api', __name__, url_prefix='/api')
gemini = GeminiService()

@api.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user, error = AuthService.register_user(username, email, password)
    if error:
        return jsonify({'error': error}), 400
    
    token = JWTManager.generate_token(user.id)
    return jsonify({'token': token, 'user_id': user.id}), 201

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400
    
    token, error = AuthService.login_user(username, password)
    if error:
        return jsonify({'error': error}), 401
    
    return jsonify({'token': token}), 200

@api.route('/materials/upload', methods=['POST'])
@JWTManager.token_required
def upload_material(user):
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    title = request.form.get('title', 'Untitled')
    
    material, error = FileHandler.save_file(file, user.id, title)
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'id': material.id,
        'title': material.title,
        'file_type': material.file_type
    }), 201

@api.route('/materials', methods=['GET'])
@JWTManager.token_required
def get_materials(user):
    materials = Material.query.filter_by(user_id=user.id).all()
    return jsonify([{
        'id': m.id,
        'title': m.title,
        'created_at': m.created_at.isoformat()
    } for m in materials]), 200

@api.route('/quiz/generate', methods=['POST'])
@JWTManager.token_required
def generate_quiz(user):
    data = request.get_json()
    material_id = data.get('material_id')
    num_questions = data.get('num_questions', 5)
    
    material = Material.query.filter_by(id=material_id, user_id=user.id).first()
    if not material:
        return jsonify({'error': 'Material not found'}), 404
    
    text = FileHandler.parse_pdf(material.file_path)
    if not text:
        return jsonify({'error': 'Could not parse file'}), 400
    
    questions = gemini.generate_quiz(text, num_questions)
    return jsonify({'questions': questions}), 201

@api.route('/summary/generate', methods=['POST'])
@JWTManager.token_required
def generate_summary(user):
    data = request.get_json()
    material_id = data.get('material_id')
    
    material = Material.query.filter_by(id=material_id, user_id=user.id).first()
    if not material:
        return jsonify({'error': 'Material not found'}), 404
    
    text = FileHandler.parse_pdf(material.file_path)
    if not text:
        return jsonify({'error': 'Could not parse file'}), 400
    
    summary = gemini.generate_summary(text)
    return jsonify({'summary': summary}), 200
