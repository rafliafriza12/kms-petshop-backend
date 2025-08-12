from flask import Blueprint, request, jsonify
from utils.jwt_middleware import token_required
from models import layanan as L

bp = Blueprint("layanan", __name__, url_prefix="/api/layanan")

@bp.get("")
def list_layanan(): return jsonify(L.list_layanan())

@bp.post("")
@token_required
def create_layanan():
    # contoh proteksi: hanya ADMIN
    if (request.user.get("role") != "ADMIN"):
        return jsonify({"status": 403,"message": "FORBIDDEN"}), 403
    data = request.json or {}
    newLayanan = L.create_layanan(data)
    return jsonify({"status": 201, "data": newLayanan, "message": "Layanan berhasil dibuat"}), 201

@bp.get("/<id>")
def get_one(id):
    doc = L.get_layanan(id)
    return (jsonify({"status": 200, "data": doc, "message": "Layanan ditemukan"}), 200) if doc else (jsonify({"status": 404,"message": "Not found"}), 404)

@bp.put("/<id>")
@token_required
def update(id): 
    if (request.user.get("role") != "ADMIN"):
        return jsonify({"status": 403,"message": "FORBIDDEN"}), 403
    doc = L.update_layanan(id, request.json or {})
    return jsonify({"status": 200, "data": doc, "message": "Layanan berhasil diedit"}), 200

@bp.delete("/<id>")
@token_required
def delete(id):
    if (request.user.get("role") != "ADMIN"):
        return jsonify({"status": 403,"message": "FORBIDDEN"}), 403
    L.delete_layanan(id)
    return jsonify({"status": 201, "message": "Layanan berhasil dihapus"}), 200
