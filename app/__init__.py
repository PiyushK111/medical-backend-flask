from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from app.models.base import db
import os

ma = Marshmallow()
migrate = Migrate()

def create_app():
    flask_app = Flask(__name__)

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql+psycopg2://postgres:piyush@db:5432/medical_db'
    )
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    flask_app.config['SECRET_KEY'] = os.getenv(
        'SECRET_KEY',
        'super-secret-key-change-me'
    )

    db.init_app(flask_app)
    ma.init_app(flask_app)
    migrate.init_app(flask_app, db)

    # Logging Configuration
    import logging
    logging.basicConfig(level=logging.INFO)
    flask_app.logger.setLevel(logging.INFO)

    # Swagger Configuration
    from flask_swagger_ui import get_swaggerui_blueprint
    SWAGGER_URL = '/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Medical Backend API"}
    )
    flask_app.register_blueprint(swaggerui_blueprint)

    # Register Blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.availability_controller import availability_bp
    from app.controllers.appointment_controller import appointment_bp
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(admin_bp)
    flask_app.register_blueprint(availability_bp)
    flask_app.register_blueprint(appointment_bp)

    # Global Error Handler
    @flask_app.errorhandler(Exception)
    def handle_exception(e):
        # Pass through HTTP errors
        if hasattr(e, 'code'):
            return {"message": str(e)}, e.code
        # Log generic errors
        flask_app.logger.error(f"Unhandled Exception: {str(e)}")
        return {"message": "Internal Server Error"}, 500

    with flask_app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from app import models


    @flask_app.route('/')
    def index():
        return {"status": "ok", "message": "Medical Backend Running"}

    return flask_app
