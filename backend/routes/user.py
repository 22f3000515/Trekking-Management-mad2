from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/api/user"
)
# User Profile Route
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

# User Dashboard Route
@user_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def user_dashboard():
   claims = get_jwt()

   if claims["role"] != "user":
        return jsonify({"message": "Access Denied"}), 403

   return jsonify({
        "message": "Welcome User Dashboard"
    }), 200
