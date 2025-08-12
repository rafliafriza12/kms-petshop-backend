import datetime as dt
from functools import wraps
import jwt
from flask import request, jsonify
from config import Config

def generate_token(payload: dict):
    exp = dt.datetime.utcnow() + dt.timedelta(minutes=Config.JWT_EXPIRES_MIN)
    token = jwt.encode({**payload, "exp": exp}, Config.JWT_SECRET, algorithm="HS256")
    return token

def verify_token(token: str):
    return jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Token diperlukan"}), 401
        token = auth_header.split(" ", 1)[1]
        try:
            payload = verify_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token kadaluarsa"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token tidak valid"}), 401
        request.user = payload  # userId, role, email
        return fn(*args, **kwargs)
    return wrapper
