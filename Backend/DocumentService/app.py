from flask import Flask
from config import Config
from model import db
from routes import bp as documents_bp
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure logging on the app instance
    app.logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    
    # Initialize the database
    db.init_app(app)
    
    # Register the documents blueprint
    app.register_blueprint(documents_bp)

    with app.app_context():
        db.drop_all()
        db.create_all()

    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", debug=True, port=5000)

