from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from Backend.App.Models.User.user_model import get_user_by_login, get_user_by_mail, get_user_by_phone, create_user


def register_user(data):
    if get_user_by_login(data["UserLogin"]).data:
        return {"msg": "Login already exists"}, 409
    if get_user_by_mail(data["mail"]).data:
        return {"msg": "Email already in use"}, 409
    if get_user_by_phone(data["TelephoneNumber"]).data:
        return {"msg": "Phone number already in use"}, 409

    data["Password"] = generate_password_hash(data["Password"])
    create_user(data)
    return {"msg": "User created"}, 201

def login_user(identifier, password):
    user = get_user_by_login(identifier)
    if not user.data:
        user = get_user_by_mail(identifier)
        if not user.data:
            return {"msg": "User not found"}, 401

    if not check_password_hash(user.data["Password"], password):
        return {"msg": "Invalid credentials"}, 401

    access_token = create_access_token(identity=user.data["UserLogin"])
    refresh_token = create_refresh_token(identity=user.data["UserLogin"])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }, 200

def refresh_token_service():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return {"access_token": new_access_token}, 200