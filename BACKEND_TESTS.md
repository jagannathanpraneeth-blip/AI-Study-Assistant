BACKEND_TESTS.md# Backend Tests and Error Handling

## Error Handling Middleware (backend/errors.py)
```python
from flask import jsonify
from werkzeug.exceptions import HTTPException

class AppError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({'error': error.message}), error.status_code
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({'error': error.description}), error.code
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({'error': 'Internal server error'}), 500
```

## Input Validation (backend/validators.py)
```python
from functools import wraps
from flask import request, jsonify

def validate_json(*required_fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Request body is empty'}), 400
            
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing field: {field}'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_file_size(max_size_mb=50):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            if file.content_length > max_size_mb * 1024 * 1024:
                return jsonify({'error': f'File too large. Max size: {max_size_mb}MB'}), 413
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

## Unit Tests (backend/tests/test_auth.py)
```python
import pytest
from app import create_app, db
from models import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

class TestAuth:
    def test_register_user(self, client):
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass'
        })
        assert response.status_code == 201
        assert 'token' in response.json
    
    def test_register_duplicate_username(self, client, app):
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'new@example.com',
            'password': 'password'
        })
        assert response.status_code == 400
    
    def test_login_success(self, client, app):
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        assert response.status_code == 200
        assert 'token' in response.json
    
    def test_login_invalid_credentials(self, client):
        response = client.post('/api/auth/login', json={
            'username': 'nonexistent',
            'password': 'wrongpass'
        })
        assert response.status_code == 401
```

## Integration Tests (backend/tests/test_materials.py)
```python
import pytest
from io import BytesIO

class TestMaterials:
    def test_upload_material_without_auth(self, client):
        response = client.post('/api/materials/upload', data={
            'file': (BytesIO(b'test'), 'test.pdf')
        })
        assert response.status_code == 401
    
    def test_upload_material_success(self, client, auth_headers):
        response = client.post('/api/materials/upload',
            headers=auth_headers,
            data={'file': (BytesIO(b'test'), 'test.pdf'), 'title': 'Test'}
        )
        assert response.status_code == 201
        assert response.json['title'] == 'Test'
    
    def test_get_materials(self, client, auth_headers):
        response = client.get('/api/materials', headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json, list)
```

## Rate Limiting (backend/rate_limit.py)
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def apply_rate_limits(app):
    limiter.init_app(app)
```

## Security Headers (backend/security.py)
```python
def init_security(app):
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
```

## pytest.ini Configuration
```ini
[pytest]
testpaths = backend/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=backend --cov-report=html --verbose
```

## Run Tests
```bash
pytest                    # Run all tests
pytest --cov             # With coverage
pytest -v               # Verbose mode
pytest backend/tests/test_auth.py   # Specific test file
```
