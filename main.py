from website import create_app
from flask_socketio import SocketIO

app = create_app()
socketio = SocketIO(app, manage_session=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)