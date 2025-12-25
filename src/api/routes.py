from flask import request, jsonify, Blueprint, current_app
from flask_cors import CORS
from api.models import db, User
from werkzeug.security import generate_password_hash
import jwt
import datetime
import os

api = Blueprint('api', __name__)
CORS(api)

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default-secret-key")


@api.route('/hello', methods=['GET'])
def handle_hello():
    return jsonify({"message": "Hello, I'm your backend"}), 200


@api.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()

        if not email or not password:
            return jsonify({"success": False, "msg": "Email and password required"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"success": False, "msg": "Email already exists"}), 409

        new_user = User(email=email)
        new_user.password = password

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "success": True,
            "msg": "User created successfully",
            "email": email
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Signup error")
        return jsonify({"success": False, "msg": "Registration failed"}), 500


@api.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()

        if not email or not password:
            return jsonify({"success": False, "msg": "Email and password required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({"success": False, "msg": "Invalid credentials"}), 401

        token = jwt.encode({
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "success": True,
            "msg": "Login successful",
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email
            }
        }), 200

    except Exception as e:
        current_app.logger.exception("Login error")
        return jsonify({"success": False, "msg": "Login failed"}), 500


@api.route('/private', methods=['GET'])
def private():
    return jsonify({
        "msg": "This is a protected route",
        "user": {
            "email": "test@example.com"  # O puedes extraerlo del token
        }
    }), 200
