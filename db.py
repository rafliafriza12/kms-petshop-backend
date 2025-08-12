from pymongo import MongoClient, ASCENDING
from config import Config

client = MongoClient(Config.MONGO_URI)

default_db = client.get_default_database()
db = default_db if default_db is not None else client["kmspetshop"]

def create_indexes():
    db.users.create_index([("email", ASCENDING)], unique=True)
    db.layanan.create_index([("kategori", ASCENDING)])
    db.kucing.create_index([("userId", ASCENDING)])
    db.keranjang.create_index([("userId", ASCENDING)], unique=True)
    db.pesanan.create_index([("userId", ASCENDING), ("statusPesanan", ASCENDING)])
