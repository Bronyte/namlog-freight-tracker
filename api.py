from flask import Blueprint, request, jsonify
from models import User, Trucks, Deliveries
from db import Database

api = Blueprint("api", __name__)


@api.get("/")
def say_hello():
    return "Hello, NamLog!"


@api.get("/api/trucks")
def get_all_trucks():
    trucks = Trucks.query.all()

    if not trucks:
        return jsonify({"error": "No trucks found"}), 404

    return jsonify([truck.to_dict() for truck in trucks]), 200


@api.get("/api/trucks/<int:id>")
def get_truck(id):
    truck = Trucks.query.get(id)

    if not truck:
        return jsonify({"error": "Truck not found"}), 404

    return jsonify(truck.to_dict()), 200


@api.post("/api/trucks")
def add_truck():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    name = data.get("name")
    registration_number = data.get("registration_number")
    status = data.get("status")

    if not name or not registration_number or not status:
        return jsonify({"error": "Missing required fields"}), 400

    new_truck = Trucks(
        name=name,
        registration_number=registration_number,
        status=status
    )

    Database.session.add(new_truck)
    Database.session.commit()

    return jsonify(new_truck.to_dict()), 201