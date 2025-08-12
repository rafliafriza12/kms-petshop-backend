from db import db
from bson import ObjectId
from datetime import datetime

COL = db.layanan
# layanan: {namaLayanan, deskripsi, benefit: [str], harga, diskon, durasiLayanan, kategori, status, createdAt, updatedAt}

def create_layanan(data):
    data["createdAt"] = data["updatedAt"] = datetime.utcnow()
    newLayanan = COL.insert_one(data)
    return COL.find_one({"_id": newLayanan.inserted_id})

def list_layanan(filters=None):
    return list(COL.find(filters or {}))

def get_layanan(id): return COL.find_one({"_id": ObjectId(id)})

def update_layanan(id, data):
    data["updatedAt"] = datetime.utcnow()
    COL.update_one({"_id": ObjectId(id)}, {"$set": data})
    return get_layanan(id)

def delete_layanan(id): COL.delete_one({"_id": ObjectId(id)})
