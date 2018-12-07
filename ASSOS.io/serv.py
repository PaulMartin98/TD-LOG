

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import random

app = Flask(__name__)

app.config['SECRET-KEY'] = 'scret'
width, height = 1000,1000
dt = 0.01
r = 5
socketio = SocketIO(app)
users = {}
bullets = []
map_state = [[-1]*width]*height



def update_map():
	# for i in range(bullets):
	# 	bullets[i] = bullets[i].move_bullet()
	for user, data in users:
		users[user]["pos"] = data["pos"]+data["speed"]*dt
	socketio.emit("update",users,broadcast = True)

@app.route('/')
def index():
	return render_template('client.html')

@socketio.on('new_connection')
def handle_new_connection():
	print("new player connected")
	id = random.randint(0,100)
	users[id] = {"pos" : [0,0],"speed" : [0,0] }
	emit('authentification',id,0,0)
	emit('users_update',users)

@socketio.on('client_speed_update')
def handle_move(user_id, speedx,speedy):
	users[user_id]['speed'] = speed


if __name__ == '__main__':
	socketio.run(app, host='localhost', port=5000)
