"""
Script para inicializar la base de datos con datos de demo
"""
from app import create_app, db
from app.models.user import User
from app.models.content import Content
from datetime import datetime

def init_database():
    """Inicializa la base de datos con datos de demo"""
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas
        print("Creando tablas de la base de datos...")
        db.create_all()
        print("✓ Tablas creadas correctamente")
        
        # Verificar si ya existe un usuario admin
        admin = User.query.filter_by(email='admin@upec.edu.ec').first()
        
        if not admin:
            print("\nCreando usuario administrador de demo...")
            # Crear usuario admin de demo
            admin = User(
                email='admin@upec.edu.ec',
                name='Administrador',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Crear usuario locutor de demo
            print("Creando usuario locutor de demo...")
            locutor = User(
                email='locutor@upec.edu.ec',
                name='Locutor Demo',
                role='locutor',
                is_active=True
            )
            locutor.set_password('locutor123')
            db.session.add(locutor)
            
            db.session.commit()
            
            print("\n" + "="*50)
            print("✓ Base de datos inicializada correctamente")
            print("="*50)
            print("\nUsuarios de demo creados:")
            print("\n1. Administrador:")
            print("   Email: admin@upec.edu.ec")
            print("   Password: admin123")
            print("\n2. Locutor:")
            print("   Email: locutor@upec.edu.ec")
            print("   Password: locutor123")
            print("\n" + "="*50)
        else:
            print("\n✓ La base de datos ya está inicializada")
            print("\nUsuarios disponibles:")
            print("   - admin@upec.edu.ec (password: admin123)")
            print("   - locutor@upec.edu.ec (password: locutor123)")

if __name__ == '__main__':
    init_database()
