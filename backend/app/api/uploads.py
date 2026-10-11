import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required
from app.utils.file_security import validate_file, save_file

ALLOWED_COVER_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB for images
MAX_PDF_SIZE = 20 * 1024 * 1024   # 20 MB for PDFs

uploads_bp = Blueprint('uploads', __name__, url_prefix='/api/uploads')

@uploads_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No se proporcionó archivo'}), 400
        
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No se seleccionó archivo'}), 400
    
    # Validate extension is .jpg or .png only
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in ALLOWED_COVER_IMAGE_EXTENSIONS:
        return jsonify({
            'error': f'Formato no permitido. Solo se aceptan: {", ".join(ALLOWED_COVER_IMAGE_EXTENSIONS)}'
        }), 400
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_IMAGE_SIZE:
        max_mb = MAX_IMAGE_SIZE / (1024 * 1024)
        return jsonify({'error': f'El archivo excede el tamaño máximo permitido de {max_mb:.0f}MB'}), 400
        
    is_valid, msg_or_filename = validate_file(file, 'image')
    if not is_valid:
        return jsonify({'error': msg_or_filename}), 400
        
    url, orig_name, size = save_file(file, current_app.config['UPLOAD_FOLDER'], 'images')
    
    return jsonify({
        'url': url,
        'originalName': orig_name,
        'sizeBytes': size
    }), 201

@uploads_bp.route('/pdf', methods=['POST'])
@jwt_required()
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No se proporcionó archivo'}), 400
        
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No se seleccionó archivo'}), 400
    
    # Validate extension is .pdf only
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext != 'pdf':
        return jsonify({'error': 'Solo se permiten archivos con extensión .pdf'}), 400
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_PDF_SIZE:
        max_mb = MAX_PDF_SIZE / (1024 * 1024)
        return jsonify({'error': f'El archivo excede el tamaño máximo permitido de {max_mb:.0f}MB'}), 400
        
    is_valid, msg_or_filename = validate_file(file, 'document')
    if not is_valid:
        return jsonify({'error': msg_or_filename}), 400
        
    url, orig_name, size = save_file(file, current_app.config['UPLOAD_FOLDER'], 'documents')
    
    return jsonify({
        'url': url,
        'originalName': orig_name,
        'sizeBytes': size
    }), 201

@uploads_bp.route('/<path:filename>', methods=['GET'])
def serve_upload(filename):
    """Serve uploaded files publicly for preview/download."""
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename)
