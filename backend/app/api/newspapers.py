import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.news import Newspaper
from app.utils.decorators import roles_required
from app.utils.file_security import validate_file, save_file

MAX_PDF_SIZE = 20 * 1024 * 1024   # 20 MB strict
ALLOWED_COVER_EXTENSIONS = {'jpg', 'jpeg', 'png'}

newspapers_bp = Blueprint('newspapers', __name__, url_prefix='/api/newspapers')

@newspapers_bp.route('', methods=['GET'])
def get_newspapers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', type=str)
    
    query = Newspaper.query
    
    if search:
        query = query.filter(Newspaper.title.ilike(f'%{search}%'))
    
    pagination = query.order_by(Newspaper.publication_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [n.to_dict() for n in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@newspapers_bp.route('/<int:id>', methods=['GET'])
def get_newspaper(id):
    """Get a single newspaper by ID."""
    newspaper = Newspaper.query.get_or_404(id)
    return jsonify(newspaper.to_dict()), 200

@newspapers_bp.route('', methods=['POST'])
@jwt_required()
@roles_required('editor', 'superadmin')
def create_newspaper():
    if 'file' not in request.files:
        return jsonify({'error': 'No se proporcionó archivo PDF'}), 400
        
    file = request.files['file']
    title = request.form.get('title')
    pub_date_str = request.form.get('publication_date')
    
    if not title or not pub_date_str or not file.filename:
        return jsonify({'error': 'Título, fecha de publicación y archivo son obligatorios'}), 400
    
    # Strict extension validation
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext != 'pdf':
        return jsonify({'error': 'Solo se permiten archivos con extensión .pdf'}), 400
    
    # Strict size validation
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_PDF_SIZE:
        max_mb = MAX_PDF_SIZE / (1024 * 1024)
        return jsonify({
            'error': f'El archivo excede el peso máximo permitido de {max_mb:.0f}MB. Tamaño actual: {file_size / (1024*1024):.2f}MB'
        }), 400
        
    try:
        pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido, use YYYY-MM-DD'}), 400
        
    is_valid, msg_or_filename = validate_file(file, 'document')
    if not is_valid:
        return jsonify({'error': msg_or_filename}), 400
        
    pdf_url, original_name, saved_file_size = save_file(file, current_app.config['UPLOAD_FOLDER'], 'documents')
    
    newspaper = Newspaper(
        title=title,
        pdf_url=pdf_url,
        publication_date=pub_date,
        file_size_bytes=saved_file_size,
        uploaded_by=get_jwt_identity()
    )
    
    # Optional cover image (only .jpg / .png)
    if 'cover' in request.files:
        cover_file = request.files['cover']
        if cover_file.filename:
            cover_ext = cover_file.filename.rsplit('.', 1)[-1].lower() if '.' in cover_file.filename else ''
            if cover_ext not in ALLOWED_COVER_EXTENSIONS:
                return jsonify({
                    'error': f'La imagen de portada solo acepta formatos: {", ".join(ALLOWED_COVER_EXTENSIONS)}'
                }), 400
            is_valid_img, _ = validate_file(cover_file, 'image')
            if is_valid_img:
                cover_url, _, _ = save_file(cover_file, current_app.config['UPLOAD_FOLDER'], 'images')
                newspaper.cover_thumbnail_url = cover_url
                
    db.session.add(newspaper)
    db.session.commit()
    
    return jsonify(newspaper.to_dict()), 201

@newspapers_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@roles_required('editor', 'superadmin')
def update_newspaper(id):
    newspaper = Newspaper.query.get_or_404(id)
    
    if 'title' in request.form:
        newspaper.title = request.form.get('title')
        
    if 'publication_date' in request.form:
        try:
            newspaper.publication_date = datetime.strptime(request.form.get('publication_date'), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido, use YYYY-MM-DD'}), 400
            
    if 'file' in request.files:
        file = request.files['file']
        if file.filename:
            ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
            if ext != 'pdf':
                return jsonify({'error': 'Solo se permiten archivos con extensión .pdf'}), 400
            
            # Size check
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            if file_size > MAX_PDF_SIZE:
                max_mb = MAX_PDF_SIZE / (1024 * 1024)
                return jsonify({
                    'error': f'El archivo excede el peso máximo permitido de {max_mb:.0f}MB'
                }), 400
            
            is_valid, msg = validate_file(file, 'document')
            if is_valid:
                pdf_url, _, saved_size = save_file(file, current_app.config['UPLOAD_FOLDER'], 'documents')
                newspaper.pdf_url = pdf_url
                newspaper.file_size_bytes = saved_size
            else:
                return jsonify({'error': msg}), 400
                
    if 'cover' in request.files:
        cover = request.files['cover']
        if cover.filename:
            cover_ext = cover.filename.rsplit('.', 1)[-1].lower() if '.' in cover.filename else ''
            if cover_ext not in ALLOWED_COVER_EXTENSIONS:
                return jsonify({
                    'error': f'La imagen de portada solo acepta formatos: {", ".join(ALLOWED_COVER_EXTENSIONS)}'
                }), 400
            is_valid, msg = validate_file(cover, 'image')
            if is_valid:
                cover_url, _, _ = save_file(cover, current_app.config['UPLOAD_FOLDER'], 'images')
                newspaper.cover_thumbnail_url = cover_url

    db.session.commit()
    return jsonify(newspaper.to_dict()), 200

@newspapers_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@roles_required('editor', 'superadmin')
def delete_newspaper(id):
    newspaper = Newspaper.query.get_or_404(id)
    db.session.delete(newspaper)
    db.session.commit()
    # Not physically deleting files here for simplicity, but could do `os.remove`
    return jsonify({'message': 'Periódico eliminado correctamente'}), 200
