from flask import Blueprint, jsonify, request
from extensions import db
from models.user import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()

    new_user = User(
        name=data['name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
        role=data['role']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201