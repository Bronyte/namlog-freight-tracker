from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, Trucks, Deliveries
from db import Database
from auth import login_required, admin_required

api = Blueprint("api", __name__)


@api.get("/")
def say_hello():
    return "Hello, NamLog!"


@api.post("/api/register")
def register_user():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username or not password or not role:
        return jsonify({
            "error": "Missing required fields: username, password and role"
        }), 400

    if role not in ["admin", "guest"]:
        return jsonify({"error": "Role must be either admin or guest"}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    new_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role=role
    )

    Database.session.add(new_user)
    Database.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": new_user.to_dict()
    }), 201



@api.post("/api/login")
def login_user():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username or not password or not role:
        return jsonify({
            "error": "Missing required fields: username, password and role"
        }), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "Invalid username, password or role"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid username, password or role"}), 401

    if user.role != role:
        return jsonify({"error": "Invalid username, password or role"}), 401

    session["user_id"] = user.id
    session["username"] = user.username
    session["role"] = user.role

    return jsonify({
        "message": "Login successful",
        "user": user.to_dict()
    }), 200


@api.post("/api/logout")
@login_required
def logout_user():
    session.clear()

    return jsonify({"message": "Logout successful"}), 200


@api.get("/api/me")
@login_required
def get_logged_in_user():
    return jsonify({
        "id": session.get("user_id"),
        "username": session.get("username"),
        "role": session.get("role")
    }), 200


@api.get("/api/users")
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@api.get("/api/users/<int:id>")
@admin_required
def get_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200



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

    return jsonify({
        "message": "Truck added successfully",
        "truck": new_truck.to_dict()
    }), 201
            

@api.get("/api/deliveries")
def get_all_deliveries():
    deliveries = Deliveries.query.all()
    return jsonify([delivery.to_dict() for delivery in deliveries]), 200


@api.get("/api/deliveries/<int:id>")
def get_delivery(id):
    delivery = Deliveries.query.get(id)

    if not delivery:
        return jsonify({"error": "Delivery not found"}), 404

    return jsonify(delivery.to_dict()), 200


@api.post("/api/deliveries")
def add_delivery():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    origin = data.get("origin")
    destination = data.get("destination")
    weight = data.get("weight")
    assigned_truck_id = data.get("assigned_truck_id")
    status = data.get("status")

    if not origin or not destination or not weight or not assigned_truck_id or not status:
        return jsonify({
            "error": "Missing required fields: origin, destination, weight, assigned_truck_id and status"
        }), 400

    truck = Trucks.query.get(assigned_truck_id)

    if not truck:
        return jsonify({"error": "Assigned truck does not exist"}), 404

    new_delivery = Deliveries(
        origin=origin,
        destination=destination,
        weight=weight,
        assigned_truck_id=assigned_truck_id,
        status=status
    )

    Database.session.add(new_delivery)
    Database.session.commit()

    return jsonify({
        "message": "Delivery added successfully",
        "delivery": new_delivery.to_dict()
    }), 201