

from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)

app.config['SECRET-KEY'] = 'scret'

socketio = SocketIO(app)

@app.route('/')
def index():
	return render_template('client.html')

@socketio.on('message')
def handle_message(msg):
	send(msg, broadcast=True)


users = []
messages_sent = {}


if __name__ == '__main__':
	socketio.run(app, host='localhost', port=5000)