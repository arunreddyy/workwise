from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import User

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config['SECRET_KEY'] = 'password12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    # Define the user_loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    # Create the database
    with app.app_context():
        db.create_all()

    return app
