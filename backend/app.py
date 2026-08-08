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

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(user_bp)

@app.route("/")
def home():
    return "Trekking Management Application V2 Backend Running"

if __name__ == "__main__":
    app.run(debug=True)