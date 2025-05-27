from App import create_app
from Backend.App.Utils.socket_instance import socketio
import logging
from Backend.App.Utils.RabbitMQ import start_rabbit_thread

logging.basicConfig(level=logging.INFO)
app = create_app()

if __name__ == '__main__':
    start_rabbit_thread()
    socketio.init_app(app)
    socketio.run(app, debug=True, port=5050)