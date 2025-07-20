from App import create_app
from flask_socketio import SocketIO
import logging

socketio = SocketIO(cors_allowed_origins=[])  # Na razie brak socketów, tylko placeholder
logging.basicConfig(level=logging.INFO)

app = create_app()

if __name__ == "__main__":
    socketio.init_app(app)
    socketio.run(app, debug=True, host="0.0.0.0", port=5050)
