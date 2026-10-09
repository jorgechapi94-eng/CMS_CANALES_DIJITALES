import pytest
import os
from app import create_app
from app.extensions import db
from app.models.user import User, Role

@pytest.fixture
def app():
    os.environ['FLASK_CONFIG'] = 'testing'
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        
        # Seed roles
        roles = ['superadmin', 'editor', 'gestor_programas']
        for r in roles:
            db.session.add(Role(name=r))
        db.session.commit()
        
        # Seed users
        superadmin = User(username='superadmin', email='superadmin@upec.edu.ec')
        superadmin.set_password('password')
        superadmin.roles.append(Role.query.filter_by(name='superadmin').first())
        
        editor = User(username='editor', email='editor@upec.edu.ec')
        editor.set_password('password')
        editor.roles.append(Role.query.filter_by(name='editor').first())
        
        gestor = User(username='gestor', email='gestor@upec.edu.ec')
        gestor.set_password('password')
        gestor.roles.append(Role.query.filter_by(name='gestor_programas').first())
        
        inactive = User(username='inactive', email='inactive@upec.edu.ec', is_active=False)
        inactive.set_password('password')
        
        db.session.add_all([superadmin, editor, gestor, inactive])
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth_headers(client):
    def _auth_headers(email='superadmin@upec.edu.ec', password='password'):
        response = client.post('/api/auth/login', json={
            'email': email,
            'password': password
        })
        token = response.json.get('access_token')
        return {'Authorization': f'Bearer {token}'}
    return _auth_headers
