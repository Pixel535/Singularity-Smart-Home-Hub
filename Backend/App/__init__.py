from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from Backend.App.config import Config

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app,
         origins=[Config.FRONTEND_ORIGIN],
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"])

    jwt.init_app(app)

    from Backend.App.Auth.Routes.auth_routes import auth_route

    app.register_blueprint(auth_route, url_prefix="/auth")

    return app