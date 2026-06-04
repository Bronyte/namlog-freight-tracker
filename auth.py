from functools import wraps
from flask import jsonify, session


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "You must be logged in"}), 401

        return function(*args, **kwargs)

    return wrapper


def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "You must be logged in"}), 401

        if session.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return function(*args, **kwargs)

    return wrapper