from datetime import datetime, timezone
import re
from app.extensions import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    
    def to_dict(self) -> dict:
        return {'id': self.id, 'name': self.name, 'slug': self.slug}

news_categories = db.Table('news_categories',
    db.Column('news_id', db.Integer, db.ForeignKey('news.id', ondelete='CASCADE'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True),
)

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String(350), unique=True, nullable=False)
    content_html = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500), nullable=True)
    cover_image_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default='draft', nullable=False)  # draft, published, archived
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    author = db.relationship('User', backref=db.backref('news_articles', lazy='dynamic'))
    categories = db.relationship('Category', secondary=news_categories, backref=db.backref('news_articles', lazy='dynamic'))
    
    @staticmethod
    def generate_slug(title: str) -> str:
        slug = title.lower().strip()
        slug = re.sub(r'[áàäâ]', 'a', slug)
        slug = re.sub(r'[éèëê]', 'e', slug)
        slug = re.sub(r'[íìïî]', 'i', slug)
        slug = re.sub(r'[óòöô]', 'o', slug)
        slug = re.sub(r'[úùüû]', 'u', slug)
        slug = re.sub(r'[ñ]', 'n', slug)
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')
    
    def to_dict(self, include_content: bool = False) -> dict:
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'cover_image_url': self.cover_image_url,
            'status': self.status,
            'author': {'id': self.author.id, 'username': self.author.username} if self.author else None,
            'categories': [c.to_dict() for c in self.categories],
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_content:
            data['content_html'] = self.content_html
        return data

class Newspaper(db.Model):
    __tablename__ = 'newspapers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    pdf_url = db.Column(db.String(500), nullable=False)
    cover_thumbnail_url = db.Column(db.String(500), nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    file_size_bytes = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    uploader = db.relationship('User', backref=db.backref('newspapers', lazy='dynamic'))
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'pdf_url': self.pdf_url,
            'cover_thumbnail_url': self.cover_thumbnail_url,
            'uploaded_by': {'id': self.uploader.id, 'username': self.uploader.username} if self.uploader else None,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'file_size_bytes': self.file_size_bytes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
