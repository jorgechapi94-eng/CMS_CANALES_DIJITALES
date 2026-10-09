import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.news import Newspaper
from app.utils.decorators import roles_required
from app.utils.file_security import validate_file, save_file

newspapers_bp = Blueprint('newspapers', __name__, url_prefix='/api/newspapers')

@newspapers_bp.route('', methods=['GET'])
def get_newspapers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = Newspaper.query.order_by(Newspaper.publication_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [n.to_dict() for n in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@newspapers_bp.route('', methods=['POST'])
@jwt_required()
@roles_required('editor', 'superadmin')
def create_newspaper():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    title = request.form.get('title')
    pub_date_str = request.form.get('publication_date')
    
    if not title or not pub_date_str or not file.filename:
        return jsonify({'error': 'Title, publication_date and file are required'}), 400
        
    try:
        pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400
        
    is_valid, msg_or_filename = validate_file(file, 'document')
    if not is_valid:
        return jsonify({'error': msg_or_filename}), 400
        
    pdf_url, original_name, file_size = save_file(file, current_app.config['UPLOAD_FOLDER'], 'documents')
    
    newspaper = Newspaper(
        title=title,
        pdf_url=pdf_url,
        publication_date=pub_date,
        file_size_bytes=file_size,
        uploaded_by=get_jwt_identity()
    )
    
    # Optional cover image
    if 'cover' in request.files:
        cover_file = request.files['cover']
        if cover_file.filename:
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
            pass
            
    if 'file' in request.files:
        file = request.files['file']
        if file.filename:
            is_valid, msg = validate_file(file, 'document')
            if is_valid:
                pdf_url, _, file_size = save_file(file, current_app.config['UPLOAD_FOLDER'], 'documents')
                newspaper.pdf_url = pdf_url
                newspaper.file_size_bytes = file_size
                
    if 'cover' in request.files:
        cover = request.files['cover']
        if cover.filename:
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
    return jsonify({'message': 'Newspaper deleted'}), 200
