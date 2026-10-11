from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.news import News, Category
from app.utils.decorators import roles_required
from app.utils.validators import sanitize_html

news_bp = Blueprint('news', __name__, url_prefix='/api/news')

ALLOWED_COVER_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def _validate_cover_url(url: str) -> tuple[bool, str]:
    """Validate that cover image URL points to an allowed format."""
    if not url:
        return True, ''
    ext = url.rsplit('.', 1)[-1].lower() if '.' in url else ''
    if ext not in ALLOWED_COVER_EXTENSIONS:
        return False, f'Formato de imagen no permitido. Solo se aceptan: {", ".join(ALLOWED_COVER_EXTENSIONS)}'
    return True, ''


@news_bp.route('', methods=['GET'])
def get_news():
    """Public endpoint: returns only published news."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', type=str)
    
    query = News.query.filter_by(status='published')
    
    if category_id:
        query = query.filter(News.categories.any(id=category_id))
        
    if search:
        query = query.filter(News.title.ilike(f'%{search}%'))
        
    query = query.order_by(News.published_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [n.to_dict() for n in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@news_bp.route('/admin', methods=['GET'])
@jwt_required()
@roles_required('editor', 'superadmin')
def get_news_admin():
    """Admin endpoint: returns all news regardless of status for the CMS panel."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status_filter = request.args.get('status', type=str)
    search = request.args.get('search', type=str)
    
    query = News.query
    
    if status_filter and status_filter in ('draft', 'published', 'archived'):
        query = query.filter_by(status=status_filter)
    
    if search:
        query = query.filter(News.title.ilike(f'%{search}%'))
        
    query = query.order_by(News.updated_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [n.to_dict(include_content=True) for n in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@news_bp.route('/<string:slug>', methods=['GET'])
def get_news_by_slug(slug):
    news = News.query.filter_by(slug=slug, status='published').first_or_404()
    return jsonify(news.to_dict(include_content=True)), 200


@news_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@roles_required('editor', 'superadmin')
def get_news_by_id(id):
    """Admin endpoint: get a single news item by ID (any status)."""
    news = News.query.get_or_404(id)
    return jsonify(news.to_dict(include_content=True)), 200


@news_bp.route('', methods=['POST'])
@jwt_required()
@roles_required('editor', 'superadmin')
def create_news():
    data = request.get_json()
    
    title = data.get('title')
    content_html = data.get('content_html')
    
    if not title or not content_html:
        return jsonify({'error': 'Title and content are required'}), 400
    
    # Validate cover image format
    cover_url = data.get('cover_image_url')
    if cover_url:
        is_valid, msg = _validate_cover_url(cover_url)
        if not is_valid:
            return jsonify({'error': msg}), 400
        
    slug = News.generate_slug(title)
    # Handle slug collisions
    base_slug = slug
    counter = 1
    while News.query.filter_by(slug=slug).first():
        slug = f'{base_slug}-{counter}'
        counter += 1
        
    sanitized_html = sanitize_html(content_html)
    
    status = data.get('status', 'draft')
    published_at = None
    if status == 'published':
        published_at = datetime.now(timezone.utc)
        
    new_news = News(
        title=title,
        slug=slug,
        content_html=sanitized_html,
        excerpt=data.get('excerpt'),
        cover_image_url=cover_url,
        status=status,
        author_id=get_jwt_identity(),
        published_at=published_at
    )
    
    category_ids = data.get('category_ids', [])
    if category_ids:
        categories = Category.query.filter(Category.id.in_(category_ids)).all()
        new_news.categories = categories
        
    db.session.add(new_news)
    db.session.commit()
    
    return jsonify(new_news.to_dict(include_content=True)), 201

@news_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@roles_required('editor', 'superadmin')
def update_news(id):
    news = News.query.get_or_404(id)
    data = request.get_json()
    
    if 'title' in data:
        news.title = data['title']
        
    if 'content_html' in data:
        news.content_html = sanitize_html(data['content_html'])
        
    if 'excerpt' in data:
        news.excerpt = data['excerpt']
        
    if 'cover_image_url' in data:
        cover_url = data['cover_image_url']
        if cover_url:
            is_valid, msg = _validate_cover_url(cover_url)
            if not is_valid:
                return jsonify({'error': msg}), 400
        news.cover_image_url = cover_url
        
    if 'status' in data:
        new_status = data['status']
        if new_status == 'published' and news.status != 'published':
            news.published_at = datetime.now(timezone.utc)
        news.status = new_status
        
    if 'category_ids' in data:
        categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
        news.categories = categories
        
    db.session.commit()
    return jsonify(news.to_dict(include_content=True)), 200

@news_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@roles_required('editor', 'superadmin')
def delete_news(id):
    news = News.query.get_or_404(id)
    news.status = 'archived'
    db.session.commit()
    return jsonify({'message': 'News archived successfully'}), 200
