from flask import Blueprint, request, jsonify
from models import User
from extensions import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)
## Register Route
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message": "Email already registered"}), 409
    
    # Create a new user object
    new_user = User(
    name=name,
    email=email,
    role="user",
    active=True
)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

## Login Route
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and Password are required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
       return jsonify({"message": "Invalid email or password"}), 401

    if not user.check_password(password):
       return jsonify({"message": "Invalid email or password"}), 401
    
    #making jwt token
    access_token = create_access_token(
    identity=str(user.id),
    additional_claims={
        "role": user.role,
        "name": user.name
    }
)
    return jsonify({
    "message": "Login successful",
    "access_token": access_token,
    "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }
}), 200
