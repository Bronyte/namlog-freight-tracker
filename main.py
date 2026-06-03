from flask import Flask, request, jsonify
from models import User, Trucks, Deliveries
from db import Database



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///namlog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Database.init_app(app)

def main():


    @app.get("/")
    def say_hello():
        return "Hello, NamLog!"

    @app.get("/api/trucks")
    def get_all_trucks():
        trucks = Trucks.query.all()
        if trucks:
            return jsonify([truck.to_dict() for truck in trucks])
        else:
            return jsonify({"error": "No trucks found"}), 404

    @app.get("/api/trucks/<int:id>")
    def get_truck(id):
            truck = Trucks.query.get(id)
            if truck:
                return jsonify(truck.to_dict())
            else:
                return jsonify({"error": "Truck not found"}), 404
            

    @app.post("/api/trucks")
    def add_truck():
        data = request.get_json()
        name = data.get("name")
        registration_number = data.get("registration_number")
        status = data.get("status")

        if not name or not registration_number or not status:
            return jsonify({"error": "Missing required fields"}), 400

        new_truck = Trucks(name=name, registration_number=registration_number, status=status)
        Database.session.add(new_truck)
        Database.session.commit()

        return jsonify(new_truck.to_dict()), 201

    
   
    app.run(debug=True)


with app.app_context():
    Database.create_all()

if __name__ == "__main__":
    main()