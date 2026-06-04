import threading
from threading import Thread


from flask import Flask

from db import Database


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///namlog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "namlog-secret-key"

Database.init_app(app)

from models import User, Trucks, Deliveries

from api import api

app.register_blueprint(api)

import os

from seed import seed_database

with app.app_context():
    db_path = os.path.join(app.instance_path, "namlog.db")

    if not os.path.exists(db_path):
        print("namlog.db not found. Creating and seeding database...")

        os.makedirs(app.instance_path, exist_ok=True)

        Database.create_all()
        seed_database()

        print("Database created and seeded successfully.")
    else:
        Database.create_all()
        print("namlog.db already exists. Seeding skipped.")

from gui import NamLogGUI

from db import test_database_singleton

def run_flask_app():
    app.run(debug=False, use_reloader=False)

def main():
    test_database_singleton()

    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()   

    NamLogGUI().mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")