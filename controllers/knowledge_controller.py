from flask import Blueprint, request, jsonify
from models.knowledge import create_or_put_knowledge
from utils.jwt_middleware import token_required
from models.admin_dashboard import get_dashboard
from bson import ObjectId

bp = Blueprint("knowledge", __name__, url_prefix="/api/knowledge")

@bp.get("")
@token_required
def get_knowledge_data():
    if (request.user.get("role") != "ADMIN"):
        return jsonify({"status": 403,"message": "FORBIDDEN"}), 403
    data = get_dashboard()
    return jsonify({"status": 200, "data": data}), 200

@bp.post("/<layanan_id>")
@token_required
def create_knowledge_data(layanan_id):
    if (request.user.get("role") != "ADMIN"):
        return jsonify({"status": 403,"message": "FORBIDDEN"}), 403
    data = request.json
    result = create_or_put_knowledge(layanan_id, data)
    return jsonify({"status": 200, "data": result}), 200
