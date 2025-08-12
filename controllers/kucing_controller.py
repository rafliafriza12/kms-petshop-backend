from flask import Blueprint, request, jsonify
from utils.jwt_middleware import token_required
from models import kucing as K
from bson import ObjectId


bp = Blueprint("kucing", __name__, url_prefix="/api/kucing")

@bp.get("")
@token_required
def list_my_cats():
    return jsonify({"status": 200, "data": K.list_kucing(request.user["userId"]), "message": "List kucing ditemukan"}), 200

@bp.post("")
@token_required
def create():
    data = request.json or {}
    data["userId"] = ObjectId(request.user["userId"])
    newCat = K.create_kucing(data)
    return jsonify({"status": 201,"data": newCat, "message": "Data kucing berhasil diinput"}), 201

@bp.put("/<id>")
@token_required
def update(id):
    updatedRow = K.update_kucing(id, request.json or {})
    return jsonify({"status": 200, "data": updatedRow, "message": "Kucing berhasil diupdate"})

@bp.delete("/<id>")
@token_required
def delete(id):
    K.delete_kucing(id); 
    return jsonify({"status": 200, "message": "Kucing berhasil dihapus"}), 200
