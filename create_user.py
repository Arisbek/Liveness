from models.services import Services, Base
from api.services.auth import get_password_hash
from dependencies.db import Engine, SessionLocal

def create_user():
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=Engine)
        
        db = SessionLocal()

        name = "admin"
        password = "master"

        # Check if user already exists
        existing_user = db.query(Services).filter(Services.owner == name).first()
        if existing_user:
            print(f"User {name} already exists!")
            return
        
        # Create user
        service = Services(
            owner=name,
            password=get_password_hash(password)
        )
        
        db.add(service)
        db.commit()
        print(f"User {name} created successfully!")
    
    except Exception as e:
        print(f"Error creating user: {str(e)}")
    
    finally:
        db.close()