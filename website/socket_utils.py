from flask_socketio import SocketIO, send

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg)