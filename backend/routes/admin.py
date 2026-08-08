from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from models import User, Trek, Booking
from extensions import db, cache
from datetime import datetime

### 1. Admin dashboard route
admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
   claims = get_jwt()

   ## Only Admin can access
   if claims["role"] != "admin":
        return jsonify({"message": "Access Denied"}), 403
   total_users = User.query.filter_by(role="user").count()
   total_staff = User.query.filter_by(role="staff").count()
   total_treks = Trek.query.count()
   total_bookings = Booking.query.count()
   return jsonify({
        "total_users": total_users,
        "total_staff": total_staff,
        "total_treks": total_treks,
        "total_bookings": total_bookings
    }), 200


### 2. Add staff route
@admin_bp.route("/add_staff", methods=["POST"])
@jwt_required()
def add_staff():
        claims = get_jwt()

        if claims["role"] != "admin":
          return jsonify({"message": "Access Denied"}), 403
    #request data
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

    # validation   
        if not name or not email or not password:
           return jsonify({"message": "All fields are required"}), 400    
        
    # Duplicate email check
        existing = User.query.filter_by(email=email).first()
        if existing:
            return jsonify({"message": "Email already exists"}), 409
        
    # add new staff
        new_staff = User(
        name=name,
        email=email,
        role="staff",
        active=True
    )
        new_staff.set_password(password)

        db.session.add(new_staff)
        db.session.commit()
        return jsonify({
          "message": "Staff added successfully"
        }), 201  


### 3. View all staff route
@admin_bp.route("/staffs", methods=["GET"])
@jwt_required()
def view_all_staff():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access Denied"}), 403

    staffs = User.query.filter_by(role="staff").all()

    staff_list = []

    for staff in staffs:
        staff_list.append({
            "id": staff.id,
            "name": staff.name,
            "email": staff.email,
            "active": staff.active
        })

    return jsonify(staff_list), 200


### 4. View all users route
@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def view_all_users():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access Denied"}), 403

    users = User.query.filter_by(role="user").all()

    user_list = []

    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "active": user.active
        })

    return jsonify(user_list), 200

### 5. Create Trek Route
@admin_bp.route("/treks", methods=["POST"])
@jwt_required()
def create_trek():
        claims = get_jwt()

        if claims["role"] != "admin":
            return jsonify({"message": "Access Denied"}), 403
        data = request.get_json()

        name = data.get("name")
        location = data.get("location")
        difficulty = data.get("difficulty")
        duration = data.get("duration")
        total_slots = data.get("total_slots")
        price = data.get("price")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
    ## Validation
        if not all([
            name,location,difficulty,duration,total_slots,price,start_date,end_date]):
            return jsonify({"message": "All fields are required"}), 400
    ## Duplicate Trek Check 
        existing_trek = Trek.query.filter_by(name=name).first()
        if existing_trek:
           return jsonify({"message": "Trek already exists"}), 409
        
    ## Difficulty Validation
        valid_difficulty = ["Easy", "Moderate", "Hard"]
        if difficulty not in valid_difficulty:
           return jsonify({
             "message": "Difficulty must be Easy, Moderate or Hard"
            }), 400

    ## Date Validation
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({
            "message": "Date format must be YYYY-MM-DD"
            }), 400

    ## Date Logic Validation
        if end_date < start_date:
            return jsonify({
            "message": "End date cannot be before start date"
            }), 400   

    ## Create Trek
        new_trek = Trek(
        name=name,location=location,difficulty=difficulty,duration=duration,
        available_slots=total_slots,total_slots=total_slots,price=price,
        start_date=start_date,end_date=end_date,status="Pending")

        db.session.add(new_trek)
        db.session.commit()     
        cache.clear()

    ## Return Response
        return jsonify({
        "message": "Trek created successfully",
        "trek_id": new_trek.id
        }), 201    


### 6. View all treks route
@admin_bp.route("/treks", methods=["GET"])
@jwt_required()
def view_all_treks():
        claims = get_jwt()

        if claims["role"] != "admin":
           return jsonify({"message": "Access Denied"}), 403 
        treks = Trek.query.all() #fetch all treks
        trek_list = []

        for trek in treks:
           trek_list.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "total_slots": trek.total_slots,
            "price": trek.price,
            "status": trek.status,
            "start_date": trek.start_date.strftime("%Y-%m-%d"),
            "end_date": trek.end_date.strftime("%Y-%m-%d"),
            "assigned_staff_id": trek.assigned_staff_id
        })

        return jsonify(trek_list), 200


### 7. Update Trek Route
@admin_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@jwt_required()
def update_trek(trek_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access Denied"}), 403
    
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    data = request.get_json() # get data from request

    # fields to update
    trek.name = data.get("name", trek.name)
    trek.location = data.get("location", trek.location)
    trek.difficulty = data.get("difficulty", trek.difficulty)
    trek.duration = data.get("duration", trek.duration)
    trek.available_slots = data.get("available_slots", trek.available_slots)
    trek.total_slots = data.get("total_slots", trek.total_slots)
    trek.price = data.get("price", trek.price)
    status = data.get("status")

    if status is not None:
        valid_status = [
          "Pending",
          "Approved",
          "Open",
          "Closed",
          "Completed"
       ]

        if status not in valid_status:
           return jsonify({
            "message": "Invalid trek status"
        }), 400

        trek.status = status
        # Date update
    if data.get("start_date"):
        trek.start_date = datetime.strptime(
            data["start_date"],
            "%Y-%m-%d"
        ).date()

    if data.get("end_date"):
        trek.end_date = datetime.strptime(
            data["end_date"],
            "%Y-%m-%d"
        ).date()

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Trek updated successfully"
    }), 200    


### 8.Delete Trek Route
@admin_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
@jwt_required()
def delete_trek(trek_id):
    claims = get_jwt() # admin checked

    if claims["role"] != "admin":
        return jsonify({"message": "Access Denied"}), 403
    trek = Trek.query.get(trek_id) # find trek by id
    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    
    # check if trek has bookings
    booking = Booking.query.filter_by(trek_id=trek_id).first() 
    if booking:
        return jsonify({
            "message": "Cannot delete trek. Bookings already exist."
        }), 400

    db.session.delete(trek) # delete trek
    db.session.commit()
    cache.clear()
    return jsonify({
        "message": "Trek deleted successfully"
    }), 200


### 9. Assign Staff to Trek Route
@admin_bp.route("/assign_staff/<int:trek_id>", methods=["PUT"])
@jwt_required()
def assign_staff(trek_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access Denied"}), 403
    data = request.get_json() # get data from request
    staff_id = data.get("staff_id")

    # Validation
    if not staff_id:
        return jsonify({
            "message": "Staff ID is required"
        }), 400
    trek = Trek.query.get(trek_id) # find trek by id
    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    # find staff by id
    staff = User.query.filter_by(id=staff_id,role="staff").first()
    if not staff:
        return jsonify({
            "message": "Staff not found"
        }), 404
    
    # Assign staff to trek
    trek.assigned_staff_id = staff.id
    db.session.commit()
    cache.clear()
    return jsonify({
        "message": "Staff assigned successfully",
        "trek_id": trek.id,
        "staff_id": staff.id,
        "staff_name": staff.name
    }), 200

### 10. View all bookings route
@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
def view_all_bookings():
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Access Denied"
        }), 403
    bookings = Booking.query.all() # fetch all bookings

    booking_list = []

    for booking in bookings:

        booking_list.append({
            "booking_id": booking.id,
            "user_id": booking.user_id,
            "user_name": booking.user.name,
            "trek_id": booking.trek_id,
            "trek_name": booking.trek.name,
            "booking_date": booking.booking_date.strftime("%Y-%m-%d %H:%M:%S"),
            "status": booking.status,
            "payment_status": booking.payment_status
        })

    return jsonify(booking_list), 200


### 11. update user status route
@admin_bp.route("/users/<int:user_id>/status", methods=["PUT"])
@jwt_required()
def update_user_status(user_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access Denied"}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    if user.role == "admin":
        return jsonify({
            "message": "Admin account cannot be deactivated"
        }), 400
    data = request.get_json()

    active = data.get("active") # validation
    if active is None:
        return jsonify({
            "message": "Active status is required"
        }), 400
    # Status update
    user.active = active

    db.session.commit()
    return jsonify({
        "message": f"{user.role.capitalize()} status updated successfully",
        "active": user.active
    }), 200


### 12.Search user 
@admin_bp.route("/search/users", methods=["GET"])
@jwt_required()
def search_users():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    name = request.args.get("name", "")

    users = User.query.filter(
        User.role=="user",
        User.name.ilike(f"%{name}%")
    ).all()

    result=[]

    for user in users:
        result.append({
            "id":user.id,
            "name":user.name,
            "email":user.email,
            "active":user.active
        })

    return jsonify(result),200


### 13. search staff
@admin_bp.route("/search/staff", methods=["GET"])
@jwt_required()
def search_staff():

    claims=get_jwt()

    if claims["role"]!="admin":
        return jsonify({"message":"Access Denied"}),403

    name = request.args.get("name", "")

    staffs=User.query.filter(
        User.role=="staff",
        User.name.ilike(f"%{name}%")
    ).all()

    result=[]

    for staff in staffs:
        result.append({
            "id":staff.id,
            "name":staff.name,
            "email":staff.email,
            "active":staff.active
        })

    return jsonify(result),200


### 14. Search trek
@admin_bp.route("/search/treks", methods=["GET"])
@jwt_required()
def search_treks():

    claims=get_jwt()

    if claims["role"]!="admin":
        return jsonify({"message":"Access Denied"}),403

    name = request.args.get("name", "")
    treks=Trek.query.filter(
        Trek.name.ilike(f"%{name}%")
    ).all()

    result=[]

    for trek in treks:
        result.append({
            "id":trek.id,
            "name":trek.name,
            "location":trek.location,
            "difficulty":trek.difficulty,
            "status":trek.status
        })

    return jsonify(result),200


### 15. Statistics route
@admin_bp.route("/statistics", methods=["GET"])
@jwt_required()
def statistics():

    claims=get_jwt()

    if claims["role"]!="admin":
        return jsonify({"message":"Access Denied"}),403

    return jsonify({
    "total_users": User.query.filter_by(role="user").count(),
    "total_staff": User.query.filter_by(role="staff").count(),
    "total_bookings": Booking.query.count(),
    "total_treks": Trek.query.count(),
    "pending": Trek.query.filter_by(status="Pending").count(),
    "approved": Trek.query.filter_by(status="Approved").count(),
    "open": Trek.query.filter_by(status="Open").count(),
    "closed": Trek.query.filter_by(status="Closed").count(),
    "completed": Trek.query.filter_by(status="Completed").count()
}),200