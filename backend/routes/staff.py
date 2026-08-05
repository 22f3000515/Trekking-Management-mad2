from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

staff_bp = Blueprint(
    "staff",
    __name__,
    url_prefix="/api/staff"
)
@staff_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def staff_dashboard():
    claims = get_jwt()

    if claims["role"] != "staff":
        return jsonify({"message": "Access Denied"}), 403
    return jsonify({
        "message": "Welcome Staff Dashboard"
    }), 200