import logging

from flask_socketio import join_room, disconnect
from flask_jwt_extended import decode_token
from Backend.App.Models.user_model import get_user_by_login
from Backend.App.Utils.socket_instance import socketio

logger = logging.getLogger(__name__)

def register_socket_events(sio):
    @sio.on("connect")
    def handle_connect(auth):
        token = (auth or {}).get("token")
        if not token:
            logger.error("[ERROR] Socket: No token provided")
            disconnect()
            return

        try:
            decoded = decode_token(token)
            identity = decoded.get("sub")

            if identity.startswith("user_session:"):
                login = identity.split(":")[1]
                user = get_user_by_login(login)
                if not user or not user.data:
                    logger.error("[ERROR] Socket: User not found")
                    disconnect()
                    return
                user_id = user.data["UserID"]
                join_room(f"user_{user_id}")
                logger.info(f"[SUCCESS] Socket: user {login} joined room user_{user_id}")

            elif identity.startswith("house_session:"):
                house_id = identity.split(":")[1]
                join_room(f"house_{house_id}")
                logger.info(f"[INFO] - Socket: house {house_id} joined room house_{house_id}")

            else:
                logger.error("[ERROR] Socket: Unknown identity format")
                disconnect()

        except Exception as e:
            logger.error(f"[ERROR] Socket: JWT decode error: {e}")
            disconnect()
