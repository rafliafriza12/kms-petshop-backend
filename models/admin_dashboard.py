from db import db
from bson import ObjectId
from datetime import datetime

USERS = db.users
KUCING = db.kucing
LAYANAN = db.layanan

def get_dashboard():    
    doc = {
        "total_users": USERS.count_documents({}),
        "total_kucing": KUCING.count_documents({}),
        "total_layanan": LAYANAN.count_documents({}),
        "ras_kucing_Populer": list(KUCING.aggregate([
            {"$group": {"_id": "$ras", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]))
    }
    return doc