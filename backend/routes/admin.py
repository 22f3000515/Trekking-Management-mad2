from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
   claims = get_jwt()

   if claims["role"] != "admin":
        return jsonify({"message": "Access Denied"}), 403
   return jsonify({
        "message": "Welcome Admin Dashboard"
    }), 200