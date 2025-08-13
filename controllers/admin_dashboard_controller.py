from flask import Blueprint, request, jsonify
from utils.jwt_middleware import token_required
from models.admin_dashboard import get_dashboard
from bson import ObjectId

bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")

@bp.get("")
@token_required
def get_dashboard_data():
    if (request.user.get("role") != "ADMIN"):
        return jsonify({"status": 403,"message": "FORBIDDEN"}), 403
    data = get_dashboard()
    return jsonify({"status": 200, "data": data}), 200
