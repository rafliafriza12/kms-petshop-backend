from flask import Blueprint, request, jsonify
from utils.jwt_middleware import token_required
from models.user import create_user, list_users, get_user, update_user, delete_user, change_password, find_by_email
from bson import ObjectId

bp = Blueprint("user", __name__, url_prefix="/api/user")

@bp.get("/")
@token_required
def get_all_users():
    """Get all users - Admin only"""
    # Check if user is admin
    if request.user.get("role") != "ADMIN":
        return jsonify({"message": "Akses ditolak. Hanya admin yang dapat melihat semua user"}), 403
    
    users = list_users()
    return jsonify({
        "status": 200,
        "data": users,
        "total": len(users)
    }), 200

@bp.post("/")
@token_required
def create_new_user():
    """Create new user - Admin only"""
    # Check if user is admin
    if request.user.get("role") != "ADMIN":
        return jsonify({"message": "Akses ditolak. Hanya admin yang dapat membuat user baru"}), 403
    
    data = request.json
    
    # Validate required fields
    required_fields = ['namaLengkap', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"Field {field} wajib diisi"}), 400
    
    # Check if email already exists
    if find_by_email(data['email']):
        return jsonify({"message": "Email sudah terdaftar"}), 409
    
    try:
        user = create_user(
            namaLengkap=data['namaLengkap'],
            email=data['email'],
            password=data['password'],
            role=data.get('role', 'USER')
        )
        # Remove password from response
        user.pop('password', None)
        
        return jsonify({
            "status": 201,
            "data": user,
            "message": "User berhasil dibuat"
        }), 201
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@bp.get("/<user_id>")
@token_required
def get_single_user(user_id):
    """Get single user - Admin or own profile"""
    # Check if user is admin or accessing own profile
    if request.user.get("role") != "ADMIN" and request.user["userId"] != user_id:
        return jsonify({"message": "Akses ditolak"}), 403
    
    try:
        user = get_user(user_id)
        if not user:
            return jsonify({"message": "User tidak ditemukan"}), 404
        
        return jsonify({
            "status": 200,
            "data": user
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@bp.put("/<user_id>")
@token_required
def update_single_user(user_id):
    """Update user - Admin or own profile"""
    # Check if user is admin or updating own profile
    if request.user.get("role") != "ADMIN" and request.user["userId"] != user_id:
        return jsonify({"message": "Akses ditolak"}), 403
    
    data = request.json
    
    # Non-admin users cannot change role
    if request.user.get("role") != "ADMIN" and 'role' in data:
        data.pop('role')
    
    # Check email uniqueness if email is being updated
    if 'email' in data:
        existing_user = find_by_email(data['email'])
        if existing_user and str(existing_user['_id']) != user_id:
            return jsonify({"message": "Email sudah digunakan oleh user lain"}), 409
    
    try:
        updated_user = update_user(user_id, data)
        if not updated_user:
            return jsonify({"message": "User tidak ditemukan"}), 404
        
        return jsonify({
            "status": 200,
            "data": updated_user,
            "message": "User berhasil diupdate"
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@bp.delete("/<user_id>")
@token_required
def delete_single_user(user_id):
    """Delete user - Admin only"""
    # Check if user is admin
    if request.user.get("role") != "ADMIN":
        return jsonify({"message": "Akses ditolak. Hanya admin yang dapat menghapus user"}), 403
    
    # Prevent admin from deleting themselves
    if request.user["userId"] == user_id:
        return jsonify({"message": "Tidak dapat menghapus akun sendiri"}), 400
    
    try:
        # Check if user exists
        user = get_user(user_id)
        if not user:
            return jsonify({"message": "User tidak ditemukan"}), 404
        
        result = delete_user(user_id)
        if result.deleted_count == 0:
            return jsonify({"message": "Gagal menghapus user"}), 500
        
        return jsonify({
            "status": 200,
            "message": "User berhasil dihapus"
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@bp.put("/<user_id>/change-password")
@token_required
def change_user_password(user_id):
    """Change user password - Admin or own profile"""
    # Check if user is admin or changing own password
    if request.user.get("role") != "ADMIN" and request.user["userId"] != user_id:
        return jsonify({"message": "Akses ditolak"}), 403
    
    data = request.json
    
    # Validate required fields
    if request.user.get("role") != "ADMIN":
        # Non-admin must provide old password
        if not data.get('oldPassword'):
            return jsonify({"message": "Password lama wajib diisi"}), 400
    
    if not data.get('newPassword'):
        return jsonify({"message": "Password baru wajib diisi"}), 400
    
    try:
        if request.user.get("role") == "ADMIN" and not data.get('oldPassword'):
            # Admin can change password without old password
            result = update_user(user_id, {"newPassword": data['newPassword']})
            if not result:
                return jsonify({"message": "User tidak ditemukan"}), 404
            return jsonify({
                "status": 200,
                "message": "Password berhasil diubah oleh admin"
            }), 200
        else:
            # Regular password change with old password verification
            result = change_password(user_id, data['oldPassword'], data['newPassword'])
            if not result['success']:
                return jsonify({"message": result['message']}), 400
            
            return jsonify({
                "status": 200,
                "message": result['message']
            }), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@bp.get("/profile/me")
@token_required
def get_my_profile():
    """Get current user's profile"""
    try:
        user = get_user(request.user["userId"])
        if not user:
            return jsonify({"message": "User tidak ditemukan"}), 404
        
        return jsonify({
            "status": 200,
            "data": user
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
