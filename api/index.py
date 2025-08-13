import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from flask import Flask, jsonify
    from flask_cors import CORS
    from config import Config
    from json_provider import BSONJSONProvider
    from db import create_indexes
    
    # Import controllers
    from controllers.auth_controller import bp as auth_bp
    from controllers.admin_dashboard_controller import bp as admin_dashboard_bp
    from controllers.knowledge_controller import bp as knowledge_bp
    from controllers.layanan_controller import bp as layanan_bp
    from controllers.kucing_controller import bp as kucing_bp
    from controllers.keranjang_controller import bp as keranjang_bp
    from controllers.pesanan_controller import bp as pesanan_bp
    from controllers.pembayaran_controller import bp as pembayaran_bp
    from controllers.user_controller import bp as user_bp

    def create_app():
        app = Flask(__name__)
        
        # Enable CORS for global access
        CORS(app, origins=["*"], supports_credentials=True)
        
        app.json_provider_class = BSONJSONProvider
        app.json = app.json_provider_class(app)
        app.config.from_object(Config)
        
        # Create indexes on app startup
        try:
            create_indexes()
        except Exception as e:
            print(f"Warning: Could not create indexes: {e}")

        @app.route("/")
        def root():
            return jsonify({
                "message": "KMS Petshop Backend API",
                "version": "1.0.0",
                "status": "running",
                "endpoints": {
                    "auth": "/api/auth",
                    "users": "/api/user", 
                    "layanan": "/api/layanan",
                    "kucing": "/api/kucing",
                    "keranjang": "/api/keranjang",
                    "pesanan": "/api/pesanan",
                    "pembayaran": "/api/pembayaran",
                    "admin": "/api/admin",
                    "knowledge": "/api/knowledge"
                }
            })

        @app.route("/health")
        def health(): 
            return jsonify({
                "status": "ok",
                "message": "Server is healthy"
            })

        # Register all blueprints
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

    # Create the Flask app
    app = create_app()

except ImportError as e:
    # Fallback for basic functionality
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route("/")
    def root():
        return jsonify({
            "message": "KMS Petshop Backend API",
            "version": "1.0.0",
            "status": "running",
            "error": f"Import error: {str(e)}"
        })
    
    @app.route("/health")
    def health():
        return jsonify({
            "status": "error",
            "message": f"Import error: {str(e)}"
        })

except Exception as e:
    # Last resort fallback
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route("/")
    def root():
        return jsonify({
            "message": "KMS Petshop Backend API",
            "version": "1.0.0", 
            "status": "error",
            "error": str(e)
        })

# For Vercel
if __name__ != '__main__':
    # This is the WSGI application that Vercel will use
    application = app
else:
    # For local development
    app.run(debug=True)
