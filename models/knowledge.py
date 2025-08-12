from db import db
from bson import ObjectId
from datetime import datetime

from models.admin_dashboard import LAYANAN

KNOWLEDGE = db.knowledge

def create_or_put_knowledge(layanan_id, data):
    knowledge = KNOWLEDGE.find_one({"layananId": ObjectId(layanan_id)})
    if knowledge:
        KNOWLEDGE.update_one({"_id": knowledge["_id"]}, {"$set": data})
        return KNOWLEDGE.find_one({"_id": knowledge["_id"]})
    data["createdAt"] = data["updatedAt"] = datetime.utcnow()
    data["layananId"] = ObjectId(layanan_id)
    newKnowledge = KNOWLEDGE.insert_one(data)
    return KNOWLEDGE.find_one({"_id": newKnowledge.inserted_id})

