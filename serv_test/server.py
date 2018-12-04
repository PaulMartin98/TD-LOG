

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import random

app = Flask(__name__)

app.config['SECRET-KEY'] = 'scret'

socketio = SocketIO(app)

@app.route('/')
def index():
	return render_template('client.html')

@socketio.on('message')
def handle_message(msg):
	print(msg)
	send(msg, broadcast=True)

@socketio.on('pingg')
def handle_pingg(json):
	print('ping')
	# send('user ' + json["user"] + 'pinged for the '
	# + json["nb_ping"] + " time", broadcast=True)
	send('user '+str(json["id"]) + ' : pong ' + str(json["vping"]),
	broadcast = True)

@socketio.on('authentification')
def handler_auth():
	id = random.randint(0,10)
	print(id)
	emit('authentification',id)


users = []
messages_sent = {}


if __name__ == '__main__':
	socketio.run(app, host='localhost', port=5000)
