import os
import PyPDF2
from werkzeug.utils import secure_filename
from models import Material, db
from datetime import datetime

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

class FileHandler:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_file(file, max_size=MAX_FILE_SIZE):
        if not file or file.filename == '':
            return False, 'No file provided'
        
        if not FileHandler.allowed_file(file.filename):
            return False, 'File type not allowed'
        
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > max_size:
            return False, f'File too large. Max size: {max_size / 1024 / 1024}MB'
        
        return True, None
    
    @staticmethod
    def save_file(file, user_id, title, upload_folder='uploads'):
        is_valid, error = FileHandler.validate_file(file)
        if not is_valid:
            return None, error
        
        filename = secure_filename(file.filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        filename = f"{user_id}_{timestamp}_{filename}"
        
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        file_size = os.path.getsize(filepath)
        file_type = filename.rsplit('.', 1)[1].lower()
        pages = FileHandler.extract_pages(filepath, file_type)
        
        material = Material(
            user_id=user_id,
            title=title,
            file_path=filepath,
            file_type=file_type,
            file_size=file_size,
            pages=pages
        )
        
        db.session.add(material)
        db.session.commit()
        
        return material, None
    
    @staticmethod
    def extract_pages(filepath, file_type):
        if file_type == 'pdf':
            try:
                with open(filepath, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    return len(pdf_reader.pages)
            except Exception:
                return None
        return None
    
    @staticmethod
    def parse_pdf(filepath):
        try:
            with open(filepath, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            return None
    
    @staticmethod
    def delete_file(material_id, user_id):
        material = Material.query.filter_by(id=material_id, user_id=user_id).first()
        if not material:
            return False, 'Material not found'
        
        try:
            if os.path.exists(material.file_path):
                os.remove(material.file_path)
            
            db.session.delete(material)
            db.session.commit()
            return True, None
        except Exception as e:
            return False, str(e)
