from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

## User Model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column( db.String(20),nullable=False, default="user")
    active = db.Column(db.Boolean,default=True )
    created_at = db.Column( db.DateTime,default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  

## Staff Model
class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),unique=True, nullable=False
    )
    contact = db.Column(db.String(15))
    experience = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20),default="Active")
    user = db.relationship("User", backref=db.backref("staff_profile", uselist=False))


## Trek Model
class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20),default="Pending")
    assigned_staff_id = db.Column( db.Integer,db.ForeignKey("users.id") )
    assigned_staff = db.relationship("User",backref="assigned_treks")   

#Booking Model
class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column( db.Integer,db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column( db.Integer, db.ForeignKey("treks.id"), nullable=False )
    booking_date = db.Column(db.DateTime,default=datetime.utcnow )
    status = db.Column( db.String(20), default="Booked" )
    payment_status = db.Column( db.String(20),default="Pending" )
    user = db.relationship("User",backref="bookings")
    trek = db.relationship( "Trek",backref="bookings")        