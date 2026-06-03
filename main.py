from flask import Flask
from db import Database



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///namlog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Database.init_app(app)

from models import User, Trucks, Deliveries

from api import api

app.register_blueprint(api)

with app.app_context():
    Database.create_all()

def main():
    app.run(debug=True)




if __name__ == "__main__":
    main()