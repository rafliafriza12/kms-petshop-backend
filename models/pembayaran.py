from db import db
from bson import ObjectId
from datetime import datetime
PAY = db.pembayaran
ORD = db.pesanan

def create_pembayaran(pesanan_id, metode, amount, status="PAID"):
    doc = {
        "pesananId": ObjectId(pesanan_id),
        "metodePembayaran": metode,
        "amount": float(amount),
        "status": status,
        "paidAt": datetime.utcnow(),
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    PAY.insert_one(doc)
    ORD.update_one({"_id": ObjectId(pesanan_id)},
                   {"$set": {"statusPembayaran": status, "statusPesanan": "CONFIRMED"}})
    return doc
