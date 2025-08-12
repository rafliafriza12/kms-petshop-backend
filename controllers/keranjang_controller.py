import logging
from flask import Blueprint, request, jsonify
from utils.jwt_middleware import token_required
from models.keranjang import get_or_create_cart, list_items, add_item, clear_items, del_one_items
from bson import ObjectId

bp = Blueprint("keranjang", __name__, url_prefix="/api/keranjang")

@bp.get("")
@token_required
def get_cart():
    cart = get_or_create_cart(request.user["userId"])
    items = list_items(cart["_id"])
    if len(items) == 0:
        return jsonify({"status": 404,  "message": "Belum ada item dikeranjang"}), 404
    total = sum(i["harga"] for i in items)
    return jsonify({"status": 200, "data": items, "totalHarga": total, "message": "List item keranjang ditemukan"}), 200

@bp.post("/items")
@token_required
def add():
    cart = get_or_create_cart(request.user["userId"])
    d = request.json or {}
    need = ["layananId","kucingId", "jadwal"]
    if not all(k in d for k in need): return jsonify({"status": 400,"message":"Data item kurang"}),400
    add_item(cart["_id"], d["layananId"], d["kucingId"], d["jadwal"])
    return jsonify({"status": 201,"message":"Layanan berhasil ditambahkan ke keranjang"}), 201

@bp.delete("/items/<id>")
def delete_one(id):
    del_one_items(id)
    return jsonify({"status": 200, "message": "Layanan berhasil dihapus dari keranjang"}), 200

@bp.delete("/items")
@token_required
def clear():
    cart = get_or_create_cart(request.user["userId"])
    clear_items(cart["_id"]); return jsonify({"status": 200, "message": "Keranjang berhasil dikosongkan"}), 200
