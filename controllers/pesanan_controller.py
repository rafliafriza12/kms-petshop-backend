from flask import Blueprint, request, jsonify
from utils.jwt_middleware import token_required
from models.keranjang import get_or_create_cart, list_items, clear_items
from models.pesanan import create_pesanan

bp = Blueprint("pesanan", __name__, url_prefix="/api/pesanan")

@bp.post("/checkout")
@token_required
def checkout():
    data = request.json
    cart = get_or_create_cart(request.user["userId"])
    items = list_items(cart["_id"])
    if not items: return jsonify({"message":"Keranjang kosong"}),400
    total = sum(i["harga"] for i in items)
    clean_items = [
        {"layananId": i["layananId"], "kucingId": i["kucingId"], "harga": i["harga"], "estimasiWaktu": i["estimasiWaktu"]}
        for i in items
    ]
    order = create_pesanan(request.user["userId"], clean_items, data["metodePembayaran"])
    clear_items(cart["_id"])
    return jsonify(order), 201

