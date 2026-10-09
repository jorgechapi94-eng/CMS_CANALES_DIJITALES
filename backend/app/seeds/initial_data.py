import click
from flask.cli import with_appcontext
from app.extensions import db
from app.models.user import User, Role
from app.models.news import Category

@click.command('seed')
@with_appcontext
def seed():
    """Seed initial data."""
    # Create roles
    roles = ['superadmin', 'editor', 'gestor_programas']
    for r in roles:
        if not Role.query.filter_by(name=r).first():
            db.session.add(Role(name=r))
            
    db.session.commit()
    
    # Create SuperAdmin
    superadmin_email = 'admin@upec.edu.ec'
    if not User.query.filter_by(email=superadmin_email).first():
        u = User(username='admin', email=superadmin_email)
        u.set_password('Admin2024!')
        superadmin_role = Role.query.filter_by(name='superadmin').first()
        u.roles.append(superadmin_role)
        db.session.add(u)
        
    # Create Categories
    categories = ['Académicas', 'Deportes', 'Cultura', 'Investigación', 'Institucional']
    for c in categories:
        slug = c.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        if not Category.query.filter_by(name=c).first():
            db.session.add(Category(name=c, slug=slug))
            
    db.session.commit()
    print("Database seeded successfully.")

def init_app(app):
    app.cli.add_command(seed)
