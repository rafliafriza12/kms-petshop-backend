from db import db
from bson import ObjectId
from datetime import datetime
from models import layanan as L

CART = db.keranjang
ITEMS = db.keranjangItem
# keranjang: {userId, createdAt, updatedAt}
# keranjangItem: {keranjangId, layananId, kucingId, harga, estimasiWaktu, createdAt, updatedAt}

def get_or_create_cart(user_id):
    cart = CART.find_one({"userId": ObjectId(user_id)})
    if cart: return cart
    doc = {"userId": ObjectId(user_id),
           "createdAt": datetime.utcnow(),
           "updatedAt": datetime.utcnow()}
    doc["_id"] = CART.insert_one(doc).inserted_id
    return doc

def list_items(cart_id):
    return list(ITEMS.aggregate([
        {"$match": {"keranjangId": ObjectId(cart_id)}},
        {"$lookup": {"from": "layanan", "localField": "layananId", "foreignField": "_id", "as": "layanan"}},
        {"$unwind": "$layanan"},
    ]))

def add_item(cart_id, layanan_id, kucing_id, jadwal):
    layanan = L.get_layanan(layanan_id)
    doc = {
        "keranjangId": ObjectId(cart_id),
        "layananId": ObjectId(layanan_id),
        "kucingId": ObjectId(kucing_id),
        "jadwal": jadwal,
        "harga": float(layanan["harga"]),
        "estimasiWaktu": int(layanan["durasiLayanan"]),
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    ITEMS.insert_one(doc); return doc

def del_one_items(id):
    ITEMS.find_one_and_delete({"_id": ObjectId(id)})

def clear_items(cart_id): ITEMS.delete_many({"keranjangId": ObjectId(cart_id)})
