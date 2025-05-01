from App import create_app
from Backend.App.Utils.socket_instance import socketio

app = create_app()

if __name__ == '__main__':
    socketio.init_app(app)
    socketio.run(app, debug=True, port=5050)