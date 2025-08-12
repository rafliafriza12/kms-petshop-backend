from db import db
from bson import ObjectId
from datetime import datetime
COL = db.kucing
# kucing: {userId, namaKucing, ras, umur, berat, tingkatAktivitas, kondisiKesehatan: [str]|None, createdAt, updatedAt}

def create_kucing(data):
    data["createdAt"] = data["updatedAt"] = datetime.utcnow()
    res = COL.insert_one(data)
    return COL.find_one({"_id": res.inserted_id})

def list_kucing(user_id): return list(COL.find({"userId": ObjectId(user_id)}))

def get_kucing(id): return COL.find_one({"_id": ObjectId(id)})

def update_kucing(id, data):
    data["updatedAt"] = datetime.utcnow()
    COL.find_one_and_update({"_id": ObjectId(id)}, {"$set": data})
    return get_kucing(id)

def delete_kucing(id): COL.find_one_and_delete({"_id": ObjectId(id)})
