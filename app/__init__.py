import os

from flask import Flask

from app.config import Config
from app.db.database import init_db


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
    )

    app.config.from_object(Config)

    # Create uploads folder if missing
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize database
    init_db()

    # Register blueprints
    from app.routes.pdf_routes import pdf_bp
    from app.routes.excel_routes import excel_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(pdf_bp)
    app.register_blueprint(excel_bp)
    app.register_blueprint(dashboard_bp)

    return app
