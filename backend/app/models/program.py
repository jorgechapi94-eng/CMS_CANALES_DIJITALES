from datetime import datetime, timezone
from app.extensions import db

class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=True)
    modality = db.Column(db.String(50), nullable=False, default='presencial')  # presencial, virtual, hibrido
    level = db.Column(db.String(50), nullable=False, default='grado')  # grado, maestria, doctorado, tecnico
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    teachers = db.relationship('ProgramTeacher', backref='program', lazy='dynamic', cascade='all, delete-orphan')
    students = db.relationship('ProgramStudent', backref='program', lazy='dynamic', cascade='all, delete-orphan')
    projects = db.relationship('ProgramProject', backref='program', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_details: bool = False) -> dict:
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'modality': self.modality,
            'level': self.level,
            'is_active': self.is_active,
            'teachers_count': self.teachers.count(),
            'students_count': self.students.count(),
            'projects_count': self.projects.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_details:
            data['teachers'] = [t.to_dict() for t in self.teachers.all()]
            data['students'] = [s.to_dict() for s in self.students.all()]
            data['projects'] = [p.to_dict() for p in self.projects.all()]
        return data

class ProgramTeacher(db.Model):
    __tablename__ = 'program_teachers'
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id', ondelete='CASCADE'), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    title_degree = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    photo_url = db.Column(db.String(500), nullable=True)
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'full_name': self.full_name,
            'title_degree': self.title_degree,
            'email': self.email,
            'photo_url': self.photo_url,
        }

class ProgramStudent(db.Model):
    __tablename__ = 'program_students'
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id', ondelete='CASCADE'), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    enrollment_year = db.Column(db.String(4), nullable=True)
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'full_name': self.full_name,
            'enrollment_year': self.enrollment_year,
        }

class ProgramProject(db.Model):
    __tablename__ = 'program_projects'
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=True)
    link_url = db.Column(db.String(500), nullable=True)
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'link_url': self.link_url,
        }
