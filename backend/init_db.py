from app import app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():

    db.create_all()  #Create all tables in the database
    admin = User.query.filter_by(email="admin@trekora.com").first()
    if not admin:
        admin = User(
            name="Admin",
            email="admin@trekora.com",
            role="admin",
            active=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully!")

    else:
        print("Admin already exists.")