from flask import Flask

from config import Config
from extensions import db, jwt


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)


@app.route("/")
def home():
    return "Trekking Management Application V2 Backend Running"


if __name__ == "__main__":
    app.run(debug=True)