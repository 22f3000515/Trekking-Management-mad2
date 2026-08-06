from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models import Trek, Booking
from extensions import db
staff_bp = Blueprint("staff", __name__)

### 1. Staff dashboard routes
@staff_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def staff_dashboard():

    claims = get_jwt()

    if claims["role"] != "staff":
        return jsonify({
            "message": "Access Denied"
        }), 403

    staff_id = int(get_jwt_identity())

    treks = Trek.query.filter_by(
        assigned_staff_id=staff_id
    ).all()

    dashboard = []

    for trek in treks:

        total_registered = Booking.query.filter_by(
            trek_id=trek.id
        ).count()

        dashboard.append({
            "trek_id": trek.id,
            "trek_name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "status": trek.status,
            "available_slots": trek.available_slots,
            "registered_users": total_registered
        })

    return jsonify(dashboard), 200


###2. Update Available Slots
@staff_bp.route("/treks/<int:trek_id>/slots", methods=["PUT"])
@jwt_required()
def update_slots(trek_id):

    claims = get_jwt()

    if claims["role"] != "staff":  # Check if the user is a staff member
        return jsonify({"message": "Access Denied"}), 403

    # Get the staff ID from the JWT identity
    staff_id = int(get_jwt_identity()) 

    trek = Trek.query.filter_by(
        id=trek_id, assigned_staff_id=staff_id).first()

    if not trek:
        return jsonify({
            "message": "Trek not found or not assigned to you"
        }), 404

    data = request.get_json()

    available_slots = data.get("available_slots")

    if available_slots is None:
        return jsonify({
            "message": "Available slots is required"
        }), 400

    # Validate that available_slots is a non-negative integer and does not exceed total_slots
    if available_slots < 0 or available_slots > trek.total_slots:
        return jsonify({
            "message": "Invalid available slots"
        }), 400

    trek.available_slots = available_slots

    db.session.commit()

    return jsonify({
        "message": "Available slots updated successfully",
        "available_slots": trek.available_slots
    }), 200


###3. Update Trek Status
@staff_bp.route("/treks/<int:trek_id>/status", methods=["PUT"])
@jwt_required()
def update_trek_status(trek_id):

    claims = get_jwt()

    # Check if the user is a staff member
    if claims["role"] != "staff": 
        return jsonify({"message": "Access Denied"}), 403

    staff_id = int(get_jwt_identity())

    trek = Trek.query.filter_by(
        id=trek_id,
        assigned_staff_id=staff_id
    ).first()

    if not trek:
        return jsonify({
            "message": "Trek not found or not assigned to you"
        }), 404

    data = request.get_json()
    # Get the status from the request data
    status = data.get("status")

    valid_status = [
        "Open",
        "Closed",
        "Started",
        "Ongoing",
        "Completed"
    ]

    if status not in valid_status:
        return jsonify({
            "message": "Invalid status"
        }), 400

    # Update the trek status
    trek.status = status

    db.session.commit()

    return jsonify({
        "message": "Trek status updated successfully",
        "status": trek.status
    }), 200


###4. View Participants
@staff_bp.route("/treks/<int:trek_id>/participants", methods=["GET"])
@jwt_required()
def view_participants(trek_id):

    claims = get_jwt()

    if claims["role"] != "staff":
        return jsonify({"message": "Access Denied"}), 403

    staff_id = int(get_jwt_identity())

    trek = Trek.query.filter_by(
        id=trek_id,
        assigned_staff_id=staff_id
    ).first()

    if not trek:
        return jsonify({
            "message": "Trek not found or not assigned to you"
        }), 404

    # Get all bookings for the trek
    bookings = Booking.query.filter_by(
        trek_id=trek.id
    ).all()

    #list of participants
    participants = []

    for booking in bookings:

        participants.append({
            "booking_id": booking.id,
            "user_id": booking.user.id,
            "name": booking.user.name,
            "email": booking.user.email,
            "booking_status": booking.status,
            "booking_date": booking.booking_date
        })

    return jsonify(participants), 200


###5. Update Participant Status
@staff_bp.route("/participants/<int:booking_id>/status", methods=["PUT"])
@jwt_required()
def update_participant_status(booking_id):

    claims = get_jwt()

    if claims["role"] != "staff":
        return jsonify({"message": "Access Denied"}), 403

    staff_id = int(get_jwt_identity())

    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    if booking.trek.assigned_staff_id != staff_id:
        return jsonify({
            "message": "You are not assigned to this trek"
        }), 403

    data = request.get_json()

    status = data.get("status")

    valid_status = [
        "Booked",
        "Completed",
        "Cancelled"
    ]

    if status not in valid_status:
        return jsonify({
            "message": "Invalid booking status"
        }), 400

    booking.status = status

    db.session.commit()

    return jsonify({
        "message": "Participant status updated successfully",
        "booking_status": booking.status
    }), 200