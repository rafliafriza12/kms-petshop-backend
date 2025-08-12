from flask import Blueprint, request, jsonify
from utils.jwt_middleware import token_required
from models.pembayaran import create_pembayaran

bp = Blueprint("pembayaran", __name__, url_prefix="/api/pembayaran")

@bp.post("")
@token_required
def pay():
    data = request.json or {}
    userId = request.user["userId"]
    need = ["metodePembayaran"]
    if not all(k in data for k in need): return jsonify({"message":"Data pembayaran kurang"}),400
    res = create_pembayaran(userId, data["items"], data["metodePembayaran"])
    return jsonify(res), 201
