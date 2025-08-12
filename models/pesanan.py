from db import db
from bson import ObjectId
from datetime import datetime

ORD = db.pesanan
ORDITEM = db.pesananItem


def create_pesanan(user_id, items, paymentMethod):
    o = {
        "userId": ObjectId(user_id),
        "totalHarga": float(sum(i["harga"] for i in items)),
        "metodePembayaran": paymentMethod,
        "statusPembayaran": "UNPAID",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    o_id = ORD.insert_one(o).inserted_id
    for it in items:
        ORDITEM.insert_one({
            "pesananId": o_id,
            "layananId": it["layananId"],
            "kucingId": it["kucingId"],
            "statusPembayaran": "UNPAID",
            "statusPesanan": "PENDING",
            "jadwal": it["jadwal"],
            "harga": it["harga"],
            "estimasiWaktu": it["estimasiWaktu"],
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        })
    return ORD.find_one({"_id": o_id})

def update_pesanan_item(pesanan_item_id, data):
    data["updatedAt"] = datetime.utcnow()
    ORDITEM.update_one({"_id": ObjectId(pesanan_item_id)}, {"$set": data})
    return ORDITEM.find_one({"_id": ObjectId(pesanan_item_id)})

def get_pesanan(pesanan_id):
    pesanan = ORD.find_one({"_id": ObjectId(pesanan_id)})
    if not pesanan:
        return None
    
    # Get pesanan items with layanan and kucing details
    items = list(ORDITEM.aggregate([
        {"$match": {"pesananId": ObjectId(pesanan_id)}},
        {"$lookup": {"from": "layanan", "localField": "layananId", "foreignField": "_id", "as": "layanan"}},
        {"$lookup": {"from": "kucing", "localField": "kucingId", "foreignField": "_id", "as": "kucing"}},
        {"$unwind": "$layanan"},
        {"$unwind": "$kucing"},
    ]))
    
    pesanan["items"] = items
    return pesanan

def list_pesanan(user_id):
    return list(ORD.aggregate([
        {"$match": {"userId": ObjectId(user_id)}},
        {"$lookup": {
            "from": "pesananItem",
            "localField": "_id",
            "foreignField": "pesananId",
            "as": "items"
        }},
        {"$addFields": {
            "totalItems": {"$size": "$items"}
        }},
        {"$sort": {"createdAt": -1}}
    ]))


