import bcrypt
from db import db
from datetime import datetime
from bson import ObjectId

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

def find_by_email(email): 
    return COL.find_one({"email": email.lower().strip()})

def find_by_id(_id): 
    return COL.find_one({"_id": ObjectId(_id)})

def list_users(filters=None):
    """Get all users with optional filters"""
    query = filters or {}
    users = list(COL.find(query))
    # Remove password from response for security
    for user in users:
        user.pop('password', None)
    return users

def get_user(user_id):
    """Get a single user by ID"""
    user = COL.find_one({"_id": ObjectId(user_id)})
    if user:
        user.pop('password', None)  # Remove password for security
    return user

def update_user(user_id, data):
    """Update user data"""
    # Remove sensitive fields that shouldn't be updated directly
    data.pop('password', None)
    data.pop('_id', None)
    
    # Handle password update separately if provided
    if 'newPassword' in data:
        data['password'] = hash_password(data.pop('newPassword'))
    
    data['updatedAt'] = datetime.utcnow()
    
    # Handle email normalization
    if 'email' in data:
        data['email'] = data['email'].lower().strip()
    
    COL.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    return get_user(user_id)

def delete_user(user_id):
    """Delete a user"""
    return COL.delete_one({"_id": ObjectId(user_id)})

def change_password(user_id, old_password, new_password):
    """Change user password with old password verification"""
    user = COL.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"success": False, "message": "User tidak ditemukan"}
    
    if not check_password(old_password, user['password']):
        return {"success": False, "message": "Password lama tidak benar"}
    
    COL.update_one(
        {"_id": ObjectId(user_id)}, 
        {"$set": {"password": hash_password(new_password), "updatedAt": datetime.utcnow()}}
    )
    return {"success": True, "message": "Password berhasil diubah"}
