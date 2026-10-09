import os
from flask import Flask
from .extensions import db, jwt, cors, migrate
from .config import config_by_name

def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*')}})
    migrate.init_app(app, db)
    
    # Ensure upload directories exist
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
    
    # Register blueprints
    from .api.auth import auth_bp
    from .api.users import users_bp
    from .api.news import news_bp
    from .api.newspapers import newspapers_bp
    from .api.programs import programs_bp
    from .api.uploads import uploads_bp
    from .api.youtube import youtube_bp
    from .api.radio import radio_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(newspapers_bp)
    app.register_blueprint(programs_bp)
    app.register_blueprint(uploads_bp)
    app.register_blueprint(youtube_bp)
    app.register_blueprint(radio_bp)
    
    # JWT callbacks
    from .models.user import User
    
    @jwt.user_identity_loader
    def user_identity_lookup(user: User) -> int:
        return user.id
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data) -> User | None:
        identity = jwt_data['sub']
        return db.session.get(User, identity)
    
    @jwt.additional_claims_loader
    def add_claims_to_access_token(user: User) -> dict:
        return {'roles': user.get_role_names(), 'email': user.email}
    
    # Token blocklist (in-memory for dev, use Redis in prod)
    BLOCKLIST = set()
    app.config['JWT_BLOCKLIST'] = BLOCKLIST
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload) -> bool:
        jti = jwt_payload['jti']
        return jti in app.config['JWT_BLOCKLIST']
    
    return app
