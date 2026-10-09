from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.program import Program, ProgramTeacher, ProgramStudent, ProgramProject
from app.utils.decorators import roles_required

programs_bp = Blueprint('programs', __name__, url_prefix='/api/programs')

@programs_bp.route('', methods=['GET'])
def get_programs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    level = request.args.get('level', type=str)
    modality = request.args.get('modality', type=str)
    
    query = Program.query.filter_by(is_active=True)
    
    if level:
        query = query.filter_by(level=level)
    if modality:
        query = query.filter_by(modality=modality)
        
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@programs_bp.route('/<int:id>', methods=['GET'])
def get_program(id):
    program = Program.query.filter_by(id=id, is_active=True).first_or_404()
    return jsonify(program.to_dict(include_details=True)), 200

@programs_bp.route('', methods=['POST'])
@jwt_required()
@roles_required('gestor_programas', 'superadmin')
def create_program():
    data = request.get_json()
    
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
        
    program = Program(
        title=title,
        description=data.get('description'),
        modality=data.get('modality', 'presencial'),
        level=data.get('level', 'grado')
    )
    db.session.add(program)
    db.session.flush() # To get program.id
    
    _process_program_relations(program, data)
    
    db.session.commit()
    return jsonify(program.to_dict(include_details=True)), 201

@programs_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@roles_required('gestor_programas', 'superadmin')
def update_program(id):
    program = Program.query.get_or_404(id)
    data = request.get_json()
    
    if 'title' in data:
        program.title = data['title']
    if 'description' in data:
        program.description = data['description']
    if 'modality' in data:
        program.modality = data['modality']
    if 'level' in data:
        program.level = data['level']
        
    _process_program_relations(program, data)
        
    db.session.commit()
    return jsonify(program.to_dict(include_details=True)), 200

@programs_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@roles_required('gestor_programas', 'superadmin')
def delete_program(id):
    program = Program.query.get_or_404(id)
    program.is_active = False
    db.session.commit()
    return jsonify({'message': 'Program archived successfully'}), 200

def _process_program_relations(program, data):
    if 'teachers' in data:
        # Clear existing
        program.teachers.delete()
        for t_data in data['teachers']:
            teacher = ProgramTeacher(
                program_id=program.id,
                full_name=t_data.get('full_name'),
                title_degree=t_data.get('title_degree'),
                email=t_data.get('email'),
                photo_url=t_data.get('photo_url')
            )
            db.session.add(teacher)
            
    if 'students' in data:
        program.students.delete()
        for s_data in data['students']:
            student = ProgramStudent(
                program_id=program.id,
                full_name=s_data.get('full_name'),
                enrollment_year=s_data.get('enrollment_year')
            )
            db.session.add(student)
            
    if 'projects' in data:
        program.projects.delete()
        for p_data in data['projects']:
            project = ProgramProject(
                program_id=program.id,
                title=p_data.get('title'),
                description=p_data.get('description'),
                link_url=p_data.get('link_url')
            )
            db.session.add(project)
