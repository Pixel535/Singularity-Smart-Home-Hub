from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from Backend.Singularity_Local.App.Routes.auth_routes import auth_route
from Backend.Singularity_Local.App.Routes.connectivity_routes import connectivity_route
from Backend.Singularity_Local.App.Routes.dashboard_routes import dashboard_route
from Backend.Singularity_Local.App.Routes.device_routes import device_route
from Backend.Singularity_Local.App.Routes.initialize_routes import initialization_route
from Backend.Singularity_Local.App.Routes.room_dashboard_routes import room_dashboard_route
from Backend.Singularity_Local.App.config import Config

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

    app.register_blueprint(initialization_route, url_prefix="/initialization")
    app.register_blueprint(connectivity_route, url_prefix="/connectivity")
    app.register_blueprint(auth_route, url_prefix="/auth")
    app.register_blueprint(dashboard_route, url_prefix="/dashboard")
    app.register_blueprint(room_dashboard_route, url_prefix="/roomDashboard")
    app.register_blueprint(device_route, url_prefix="/device")

    return app
