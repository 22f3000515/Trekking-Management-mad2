from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity
)

from models import Trek, Booking
from extensions import db


staff_bp = Blueprint(
    "staff",
    __name__,
    url_prefix="/api/staff"
)


# =========================================================
# 1. STAFF DASHBOARD
# =========================================================

@staff_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def staff_dashboard():

    claims = get_jwt()

    if claims["role"] != "staff":
        return jsonify({
            "message": "Access Denied"
        }), 403

    staff_id = int(get_jwt_identity())

    # Get only treks assigned to this staff member
    treks = Trek.query.filter_by(
        assigned_staff_id=staff_id
    ).all()

    dashboard = []

    for trek in treks:

        # Total participants excluding cancelled bookings
        total_registered = Booking.query.filter(
            Booking.trek_id == trek.id,
            Booking.status != "Cancelled"
        ).count()

        # Currently booked participants
        total_booked = Booking.query.filter_by(
            trek_id=trek.id,
            status="Booked"
        ).count()

        # Completed participants
        total_completed = Booking.query.filter_by(
            trek_id=trek.id,
            status="Completed"
        ).count()

        # Cancelled participants
        total_cancelled = Booking.query.filter_by(
            trek_id=trek.id,
            status="Cancelled"
        ).count()

        dashboard.append({

            "trek_id": trek.id,
            "trek_name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,

            "status": trek.status,

            "total_slots": trek.total_slots,
            "available_slots": trek.available_slots,

            "registered_users": total_registered,
            "booked_users": total_booked,
            "completed_users": total_completed,
            "cancelled_users": total_cancelled
        })

    return jsonify(dashboard), 200


# =========================================================
# 2. UPDATE AVAILABLE SLOTS
# =========================================================

@staff_bp.route(
    "/treks/<int:trek_id>/slots",
    methods=["PUT"]
)
@jwt_required()
def update_slots(trek_id):

    claims = get_jwt()

    if claims["role"] != "staff":
        return jsonify({
            "message": "Access Denied"
        }), 403

    staff_id = int(get_jwt_identity())

    # Make sure trek belongs to this staff member
    trek = Trek.query.filter_by(
        id=trek_id,
        assigned_staff_id=staff_id
    ).first()

    if not trek:
        return jsonify({
            "message": "Trek not found or not assigned to you"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request data is required"
        }), 400

    available_slots = data.get("available_slots")

    if available_slots is None:
        return jsonify({
            "message": "Available slots is required"
        }), 400

    # Make sure value is an integer
    if not isinstance(available_slots, int):
        return jsonify({
            "message": "Available slots must be an integer"
        }), 400

    # Validation
    if available_slots < 0:
        return jsonify({
            "message": "Available slots cannot be negative"
        }), 400

    if available_slots > trek.total_slots:
        return jsonify({
            "message": "Available slots cannot exceed total slots"
        }), 400

    trek.available_slots = available_slots

    db.session.commit()

    return jsonify({
        "message": "Available slots updated successfully",
        "available_slots": trek.available_slots
    }), 200


# =========================================================
# 3. UPDATE TREK STATUS
# =========================================================

@staff_bp.route(
    "/treks/<int:trek_id>/status",
    methods=["PUT"]
)
@jwt_required()
def update_trek_status(trek_id):

    claims = get_jwt()

    if claims["role"] != "staff":
        return jsonify({
            "message": "Access Denied"
        }), 403

    staff_id = int(get_jwt_identity())

    # Make sure trek belongs to this staff member
    trek = Trek.query.filter_by(
        id=trek_id,
        assigned_staff_id=staff_id
    ).first()

    if not trek:
        return jsonify({
            "message": "Trek not found or not assigned to you"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request data is required"
        }), 400

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

    # Update trek status
    trek.status = status

    # If trek is completed,
    # automatically complete all active bookings
    if status == "Completed":

        bookings = Booking.query.filter_by(
            trek_id=trek.id
        ).all()

        for booking in bookings:

            if booking.status == "Booked":
                booking.status = "Completed"

    db.session.commit()

    return jsonify({
        "message": "Trek status updated successfully",
        "status": trek.status
    }), 200


# =========================================================
# 4. VIEW PARTICIPANTS
# =========================================================

@staff_bp.route(
    "/treks/<int:trek_id>/participants",
    methods=["GET"]
)
@jwt_required()
def view_participants(trek_id):

    claims = get_jwt()

    if claims["role"] != "staff":
        return jsonify({
            "message": "Access Denied"
        }), 403

    staff_id = int(get_jwt_identity())

    # Only assigned staff can see participants
    trek = Trek.query.filter_by(
        id=trek_id,
        assigned_staff_id=staff_id
    ).first()

    if not trek:
        return jsonify({
            "message": "Trek not found or not assigned to you"
        }), 404

    bookings = Booking.query.filter_by(
        trek_id=trek.id
    ).all()

    participants = []

    for booking in bookings:

        participants.append({

            "booking_id": booking.id,

            "user_id": booking.user.id,

            "name": booking.user.name,

            "email": booking.user.email,

            "booking_status": booking.status,

            "booking_date": booking.booking_date,

            "trek_name": trek.name,

            "trek_status": trek.status
        })

    return jsonify(participants), 200


# =========================================================
# 5. UPDATE PARTICIPANT STATUS
# =========================================================

@staff_bp.route(
    "/participants/<int:booking_id>/status",
    methods=["PUT"]
)
@jwt_required()
def update_participant_status(booking_id):

    claims = get_jwt()

    if claims["role"] != "staff":
        return jsonify({
            "message": "Access Denied"
        }), 403

    staff_id = int(get_jwt_identity())

    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({
            "message": "Booking not found"
        }), 404

    # Make sure this booking belongs to
    # a trek assigned to the logged-in staff
    if booking.trek.assigned_staff_id != staff_id:
        return jsonify({
            "message": "You are not assigned to this trek"
        }), 403

    # Cancelled booking cannot be changed
    if booking.status == "Cancelled":
        return jsonify({
            "message": "Cancelled booking cannot be changed"
        }), 400

    # Completed booking cannot be changed
    if booking.status == "Completed":
        return jsonify({
            "message": "Completed booking cannot be changed"
        }), 400

    # A completed trek should not allow
    # changing participant status
    if booking.trek.status == "Completed":
        return jsonify({
            "message": "Participants cannot be changed after trek completion"
        }), 400

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request data is required"
        }), 400

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