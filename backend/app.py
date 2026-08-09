from flask import Flask
from flask_cors import CORS

from routes import auth_bp, admin_bp, staff_bp, user_bp
from config import Config
from extensions import db, jwt, mail, cache

app = Flask(__name__)
app.config.from_object(Config)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "http://localhost:5173"
        }
    }
)

cache.init_app(app, config={
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_URL": "redis://localhost:6379/0",
    "CACHE_DEFAULT_TIMEOUT": 300
})

db.init_app(app)
jwt.init_app(app)
mail.init_app(app)


@jwt.token_in_blocklist_loader
def check_if_user_is_active(jwt_header, jwt_payload):
    from models import User

    user_id = jwt_payload.get("sub")
    user = User.query.get(int(user_id)) if user_id else None

    return user is None or not user.active

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(user_bp)

@app.route("/")
def home():
    return "Trekking Management Application V2 Backend Running"

if __name__ == "__main__":
    app.run(debug=True)