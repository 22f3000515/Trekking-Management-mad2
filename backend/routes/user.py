import os
from flask import Blueprint, jsonify, request, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models import User, Trek, Booking
from extensions import db, cache

user_bp = Blueprint(
    "user",__name__,
    url_prefix="/api/user"
)
### 1. User Profile Route
@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
   user_id = get_jwt_identity()
   claims = get_jwt()
   return jsonify({
        "message": "Protected Route Working",
        "user_id": user_id,
        "name": claims["name"],
        "role": claims["role"]
    }), 200


### 2.User Dashboard Route
@user_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():

    claims = get_jwt()

    if claims["role"] != "user":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "active": user.active
    }), 200


### 3.View Available Treks
@user_bp.route("/treks", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def view_treks():

    claims = get_jwt()

    if claims["role"] != "user":
        return jsonify({"message": "Access Denied"}), 403

    treks = Trek.query.filter_by(status="Open").all()

    # Prepare the result list
    result = []

    for trek in treks:
        result.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "price": trek.price,
            "available_slots": trek.available_slots,
            "start_date": trek.start_date,
            "end_date": trek.end_date,
            "status": trek.status
        })

    return jsonify(result), 200

### 4.Book Trek
@user_bp.route("/book/<int:trek_id>", methods=["POST"])
@jwt_required()
def book_trek(trek_id):

    claims = get_jwt()

    if claims["role"] != "user":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    if trek.status != "Open":
        return jsonify({
            "message": "Booking allowed only for Open treks"
        }), 400
    
    # Check if there are available slots
    if trek.available_slots <= 0:
        return jsonify({
            "message": "No slots available"
        }), 400
    
    # Check if the user has already booked this trek
    existing_booking = Booking.query.filter(
     Booking.user_id == user_id,
     Booking.trek_id == trek_id,
     Booking.status != "Cancelled"
    ).first()

    if existing_booking:
        return jsonify({
            "message": "You have already booked this trek"
        }), 409
    # Create a new booking
    booking = Booking(
        user_id=user_id,
        trek_id=trek_id,
        status="Booked"
    )
    db.session.add(booking)

    # Decrease the available slots of the trek
    trek.available_slots -= 1
    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Trek booked successfully"
    }), 201


### 5.Update User Profile
@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    claims = get_jwt()

    if claims["role"] != "user":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    # Get the user from the database
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    # Update the user's profile
    if name:
        user.name = name

    if email:
        existing_user = User.query.filter(
            User.email == email,
            User.id != user_id
        ).first()

        if existing_user:
            return jsonify({
                "message": "Email already exists"
            }), 409

        user.email = email

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }), 200


### 6.Search and Filter Treks
@user_bp.route("/search", methods=["GET"])
@jwt_required()
def search_treks():

    claims = get_jwt()

    if claims["role"] != "user":
        return jsonify({"message": "Access Denied"}), 403

    query = Trek.query.filter(Trek.status == "Open")

    location = request.args.get("location")
    difficulty = request.args.get("difficulty")
    duration = request.args.get("duration")
    name = request.args.get("name")

    # Apply filters based on query parameters
    if name:
        query = query.filter(Trek.name.ilike(f"%{name}%"))
    if location:
        query = query.filter(Trek.location.ilike(f"%{location}%"))

    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)

    if duration:
        try:
          query = query.filter(Trek.duration == int(duration))
        except ValueError:
          return jsonify({"message": "Invalid duration"}), 400
    # Get the filtered treks
    treks = query.all() 

    result = []

    for trek in treks:
        result.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "price": trek.price,
            "available_slots": trek.available_slots,
            "start_date": trek.start_date,
            "end_date": trek.end_date,
            "status": trek.status
        })

    return jsonify(result), 200

### 7. My Booking History
@user_bp.route("/bookings", methods=["GET"])
@jwt_required()
def booking_history():

    claims = get_jwt()

    if claims["role"] != "user":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    bookings = Booking.query.filter_by(user_id=user_id).all()

    result = []
    
    for booking in bookings:
       result.append({
        "booking_id": booking.id,
        "trek_name": booking.trek.name,
        "location": booking.trek.location,
        "difficulty": booking.trek.difficulty,
        "duration": booking.trek.duration, 
        "price": booking.trek.price,
          "trek_status": booking.trek.status,
        "available_slots": booking.trek.available_slots,
        "total_slots": booking.trek.total_slots,
        "booking_date": booking.booking_date,
        "booking_status": booking.status,
        "payment_status": booking.payment_status,
       "start_date": booking.trek.start_date,
       "end_date": booking.trek.end_date
})

    return jsonify(result), 200

### 8. Export Booking History
@user_bp.route("/bookings/export", methods=["POST"])
@jwt_required()
def export_booking_history():

    claims = get_jwt()

    if claims["role"] != "user":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    from celery_app import export_booking_history_task

    task = export_booking_history_task.delay(user_id)

    return jsonify({
        "message": "CSV export started successfully",
        "task_id": task.id
    }), 202


### 8b. Check Export Task Status
@user_bp.route("/bookings/export/status/<task_id>", methods=["GET"])
@jwt_required()
def export_booking_status(task_id):

    from celery_app import celery

    task = celery.AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "state": task.state
    }

    if task.state == "SUCCESS":
        # export_booking_history_task returns the CSV filename
        response["filename"] = task.result
        response["download_url"] = f"/api/user/bookings/export/download/{task.result}"
    elif task.state == "FAILURE":
        response["error"] = str(task.result)

    return jsonify(response), 200


### 8c. Download Exported CSV
@user_bp.route("/bookings/export/download/<path:filename>", methods=["GET"])
@jwt_required()
def download_booking_export(filename):

    export_dir = os.path.join(current_app.root_path, "exports")

    return send_from_directory(
        export_dir,
        filename,
        as_attachment=True
    )

### 9. Cancel Booking
@user_bp.route("/bookings/<int:booking_id>/cancel", methods=["PUT"])
@jwt_required()
def cancel_booking(booking_id):

    claims = get_jwt()

    if claims["role"] != "user":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    # Get the booking from the database
    booking = Booking.query.filter_by(
        id=booking_id,
        user_id=user_id
    ).first()

    if not booking:
        return jsonify({
            "message": "Booking not found"
        }), 404

    if booking.status == "Cancelled":
        return jsonify({
            "message": "Booking already cancelled"
        }), 400

    if booking.status == "Completed":
        return jsonify({
            "message": "Completed booking cannot be cancelled"
        }), 400

    booking.status = "Cancelled"
    # Increase the available slots of the trek
    booking.trek.available_slots += 1

    db.session.commit()
    cache.clear()
    # Return the updated booking details 
    return jsonify({
        "message": "Booking cancelled successfully",
        "booking_id": booking.id,
        "booking_status": booking.status,
        "available_slots": booking.trek.available_slots
    }), 200