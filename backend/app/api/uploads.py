from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.utils.file_security import validate_file, save_file

uploads_bp = Blueprint('uploads', __name__, url_prefix='/api/uploads')

@uploads_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400
        
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
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400
        
    is_valid, msg_or_filename = validate_file(file, 'document')
    if not is_valid:
        return jsonify({'error': msg_or_filename}), 400
        
    url, orig_name, size = save_file(file, current_app.config['UPLOAD_FOLDER'], 'documents')
    
    return jsonify({
        'url': url,
        'originalName': orig_name,
        'sizeBytes': size
    }), 201
