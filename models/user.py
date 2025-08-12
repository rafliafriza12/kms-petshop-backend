import bcrypt
from db import db
from datetime import datetime

COL = db.users

def hash_password(raw: str) -> bytes:
    return bcrypt.hashpw(raw.encode(), bcrypt.gensalt())

def check_password(raw: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(raw.encode(), hashed)

def create_user(namaLengkap, email, password, role="USER"):
    doc = {
        "namaLengkap": namaLengkap,
        "email": email.lower().strip(),
        "password": hash_password(password),
        "role": role,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    res = COL.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc

def find_by_email(email): return COL.find_one({"email": email.lower().strip()})
def find_by_id(_id): return COL.find_one({"_id": _id})
