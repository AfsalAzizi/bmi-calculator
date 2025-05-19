from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production

    # Register blueprints
    from app.routes.bmi_routes import bmi_bp
    app.register_blueprint(bmi_bp)

    return app
