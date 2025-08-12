from flask import Blueprint, request, jsonify
from models.user import create_user, find_by_email, check_password
from utils.jwt_middleware import generate_token

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

ALLOWED_ROLES = {"USER", "ADMIN"}

@bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    # validasi field wajib (tidak boleh kosong)
    required = ("namaLengkap", "email", "password")
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"status": 400, "message": f"Field {', '.join(missing)} wajib"}), 400

    email = data["email"].strip().lower()
    if find_by_email(email):
        return jsonify({"status": 409, "message": "Email sudah terdaftar"}), 409

    # role opsional -> default USER; terima hanya USER/ADMIN (case-insensitive)
    role = (data.get("role") or "USER").strip().upper()
    if role not in ALLOWED_ROLES:
        return jsonify({"status": 400, "message": "Role tidak sesuai"}), 400

    create_user(
        namaLengkap=data["namaLengkap"],
        email=email,
        password=data["password"],
        role=role,
    )
    return jsonify({"status": 201, "message": "Akun berhasil didaftarkan"}), 201

@bp.post("/login")
def login():
    data = request.json or {}
    user = find_by_email(data.get("email",""))
    if not user: 
        return jsonify({"status": 401,"message": "Email/password salah"}), 401
    if not check_password(data.get("password",""), user["password"]):
        return jsonify({"status": 401,"message": "Email/password salah"}), 401

    token = generate_token({
        "userId": str(user["_id"]),
        "email": user["email"],
        "role": user.get("role","USER")
    })

    # HANYA kirim field yang aman & serializable
    public_user = {
        "_id": str(user["_id"]),
        "namaLengkap": user.get("namaLengkap"),
        "email": user.get("email"),
        "role": user.get("role"),
        "token": token,
        "createdAt": user.get("createdAt").isoformat() if user.get("createdAt") else None,
        "updatedAt": user.get("updatedAt").isoformat() if user.get("updatedAt") else None,
    }

    return jsonify({"status": 200,"data": public_user, "message": "Login berhasil"}), 200

