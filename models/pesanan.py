from db import db
from bson import ObjectId
from datetime import datetime

ORD = db.pesanan
ORDITEM = db.pesananItem


def create_pesanan(user_id, items, paymentMethod):
    o = {
        "userId": ObjectId(user_id),
        "totalHarga": float(sum(items["harga"] for i in items)),
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

# def