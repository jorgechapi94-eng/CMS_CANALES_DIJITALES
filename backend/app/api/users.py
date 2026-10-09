from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.user import User, Role
from app.utils.decorators import roles_required
from app.utils.validators import validate_upec_email

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('', methods=['GET'])
@jwt_required()
@roles_required('superadmin')
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [user.to_dict() for user in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@users_bp.route('', methods=['POST'])
@jwt_required()
@roles_required('superadmin')
def create_user():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    roles_data = data.get('roles', [])

    if not email or not username or not password:
        return jsonify({'error': 'Email, username, and password are required'}), 400

    if not validate_upec_email(email):
        return jsonify({'error': 'Sólo se permiten correos @upec.edu.ec'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
        
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    if roles_data:
        roles = Role.query.filter(Role.name.in_(roles_data)).all()
        new_user.roles = roles

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

@users_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@roles_required('superadmin')
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    if 'is_active' in data:
        user.is_active = data['is_active']
        
    if 'roles' in data:
        roles = Role.query.filter(Role.name.in_(data['roles'])).all()
        user.roles = roles

    db.session.commit()
    return jsonify(user.to_dict()), 200

@users_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@roles_required('superadmin')
def delete_user(id):
    user = User.query.get_or_404(id)
    user.is_active = False
    db.session.commit()
    return jsonify({'message': 'User soft deleted'}), 200
