from flask import Flask
from routes import auth_bp, admin_bp, staff_bp, user_bp
from config import Config
from extensions import db, jwt, mail

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app) # Initialize SQLAlchemy with the app
jwt.init_app(app) # Initialize Flask-JWT-Extended with the app
mail.init_app(app) # Initialize Flask-Mail with the app
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(user_bp)


@app.route("/")
def home():
    return "Trekking Management Application V2 Backend Running"


if __name__ == "__main__":
    app.run(debug=True)