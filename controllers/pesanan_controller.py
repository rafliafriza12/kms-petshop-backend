from flask import Blueprint, request, jsonify
from utils.jwt_middleware import token_required
from models.keranjang import get_or_create_cart, list_items, clear_items
from models.pesanan import create_pesanan, update_pesanan_item, get_pesanan, list_pesanan

bp = Blueprint("pesanan", __name__, url_prefix="/api/pesanan")

@bp.post("/checkout")
@token_required
def checkout():
    data = request.json
    cart = get_or_create_cart(request.user["userId"])
    items = list_items(cart["_id"])
    if not items: return jsonify({"message":"Keranjang kosong"}),400
    clean_items = [
        {"layananId": i["layananId"], "kucingId": i["kucingId"], "harga": i["harga"], "estimasiWaktu": i["estimasiWaktu"], "jadwal": i.get("jadwal")}
        for i in items
    ]
    order = create_pesanan(request.user["userId"], clean_items, data["metodePembayaran"])
    clear_items(cart["_id"])
    return jsonify(order), 201

@bp.put("/item/<pesanan_item_id>")
@token_required
def update(pesanan_item_id):
    data = request.json
    pesanan = update_pesanan_item(pesanan_item_id, data)
    if not pesanan:
        return jsonify({"message": "Pesanan tidak ditemukan"}), 404
    return jsonify({"status": 200, "data": pesanan}), 200

@bp.get("/")
@token_required
def get_all_pesanan():
    pesanan_list = list_pesanan(request.user["userId"])
    
    # Count orders by status
    pending_count = sum(1 for p in pesanan_list for item in p['items'] if item.get("statusPesanan") == "PENDING")
    proses_count = sum(1 for p in pesanan_list for item in p['items'] if item.get("statusPesanan") == "PROSES")
    selesai_count = sum(1 for p in pesanan_list for item in p['items'] if item.get("statusPesanan") == "SELESAI")

    # Calculate total transaction amount
    total_transaksi = sum(p.get("totalHarga", 0) for p in pesanan_list)

    return jsonify({
        "status": 200,
        "data": pesanan_list,
        "summary": {
            "pending": pending_count,
            "proses": proses_count,
            "selesai": selesai_count,
            "total_transaksi": total_transaksi
        }
    }), 200

@bp.get("/<pesanan_id>")
@token_required
def get_single_pesanan(pesanan_id):
    pesanan = get_pesanan(pesanan_id)
    if not pesanan:
        return jsonify({"message": "Pesanan tidak ditemukan"}), 404
    
    # Check if pesanan belongs to the authenticated user
    if str(pesanan["userId"]) != request.user["userId"]:
        return jsonify({"message": "Akses ditolak"}), 403
    
    return jsonify({
        "status": 200,
        "data": pesanan
    }), 200

