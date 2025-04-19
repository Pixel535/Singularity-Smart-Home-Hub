from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from Backend.App.Routes.house_routes import house_route
from Backend.App.config import Config

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app,
         resources={r"/*": {"origins": Config.FRONTEND_ORIGIN}},
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-CSRF-TOKEN"])

    jwt.init_app(app)

    from Backend.App.Routes.auth_routes import auth_route
    from Backend.App.Routes.dashboard_routes import dashboard_route
    from Backend.App.Routes.profile_routes import profile_route
    from Backend.App.Routes.house_routes import house_route

    app.register_blueprint(auth_route, url_prefix="/auth")
    app.register_blueprint(dashboard_route, url_prefix="/dashboard")
    app.register_blueprint(profile_route, url_prefix="/profile")
    app.register_blueprint(house_route, url_prefix="/house")

    return app
