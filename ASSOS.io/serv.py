

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import random

app = Flask(__name__)

app.config['SECRET-KEY'] = 'scret'
width, height = 1000,1000
dt = 0.01
r = 5
socketio = SocketIO(app)

players = {}
bullets = []
map_state = [[-1]*width]*height

@app.route('/')
def index():
	return render_template('client_game.html')

@socketio.on('new_connection')
def handle_new_connection():
	print("new player connected")
	id = random.randint(0,100)
	print(id)
	users[id] = {"x" :0, "y" : 0, "vx" : 0,"vy" : 0 }
	emit('authentification',id,0,0)

@socketio.on('client_speed_update')
def handle_move(user_id, vx, vy):
	users[user_id]['speed'] = speed

@socketio.on('client_request')
def handle_client_request():
  socket.emit('server_update',players, broadcast = True)



if __name__ == '__main__':
	# app.debug = True
	socketio.run(app, host='localhost', port=5000)
