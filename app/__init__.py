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

    db.init_app(flask_app)
    ma.init_app(flask_app)
    migrate.init_app(flask_app, db)

    with flask_app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from app import models
        
        # Create tables
        db.create_all()

    @flask_app.route('/')
    def index():
        return {"status": "ok", "message": "Medical Backend Running"}

    return flask_app
