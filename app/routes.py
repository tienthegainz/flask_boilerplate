from flask import request, jsonify
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.schemas import UserSchema, UserLoginSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = UserLoginSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify(message='Invalid username or password'), 401


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # JWTs are stateless, so logout can be handled client-side by discarding the token
    return jsonify(message='Successfully logged out'), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = UserSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    hashed_password = generate_password_hash(data['password'], method='scrypt')
    new_user = User(username=data['username'], password=hashed_password, address=data['address'])
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        return jsonify(message=err), 400
    return jsonify(message='User registered successfully'), 201

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200
