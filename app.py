from flask import Flask, jsonify
from config import Config
from json_provider import BSONJSONProvider
from db import create_indexes
from controllers.auth_controller import bp as auth_bp
from controllers.admin_dashoard_controller import bp as admin_dashboard_bp
from controllers.knowledge_controller import bp as knowledge_bp
from controllers.layanan_controller import bp as layanan_bp
from controllers.kucing_controller import bp as kucing_bp
from controllers.keranjang_controller import bp as keranjang_bp
from controllers.pesanan_controller import bp as pesanan_bp
from controllers.pesanan_controller import bp as pesanan_bp
from controllers.pembayaran_controller import bp as pembayaran_bp
from controllers.user_controller import bp as user_bp

def create_app():
    app = Flask(__name__)
    app.json_provider_class = BSONJSONProvider
    app.json = app.json_provider_class(app)
    app.config.from_object(Config)
    create_indexes()

    @app.get("/health")
    def health(): return jsonify({"status": "ok"})

    app.register_blueprint(auth_bp)
    app.register_blueprint(layanan_bp)
    app.register_blueprint(kucing_bp)
    app.register_blueprint(keranjang_bp)
    app.register_blueprint(pesanan_bp)
    app.register_blueprint(pembayaran_bp)
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(knowledge_bp)
    app.register_blueprint(user_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
