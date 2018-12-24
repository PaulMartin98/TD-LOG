

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import random
import time as time
from math import *

app = Flask(__name__)

app.config['SECRET-KEY'] = 'scret'
width, height = 1000,1000
dt = 0.005
r = 5
socketio = SocketIO(app)

Xstart , Ystart = 200,200
speed = 0.005
bullet_speed = 0.01
players = {}
bullets = {}

server_clock = time.clock()
last_update = server_clock

@app.route('/')
def index():
	return render_template('client_game2.html')

@socketio.on('new_connection')
def handle_new_connection():
	print("new player connected")
	id = random.randint(0,100)
	print(id)
	players[id] = {"x" :Xstart, "y" : Ystart, "vx" : 0,"vy" : 0 }
	emit('authentification',id)

@socketio.on('client_speed_update')
def handle_move(id,vx,vy):
	# print('update',vx,vy)
	players[id]['vx'] = vx
	players[id]['vy'] = vy
	# print(players)
@socketio.on('client_shoot')
def handle_shoot(id,vx,vy):
	print('shoot !',id)
	bullet_id = random.randint(100,200)
	bullets[bullet_id] = {"x" :players[id]["x"],
	"y" : players[id]["y"], "vx" : vx ,"vy" : vy }

def players_update(last_update):
	server_clock = time.clock()
	print(bullets)
	for id in players:
		players[id]["x"] = players[id]["x"]+players[id]["vx"]*(server_clock-last_update)*speed
		players[id]["y"] = players[id]["y"]+players[id]["vy"]*(server_clock-last_update)*speed
	for id in bullets:
		bullets[id]["x"] = bullets[id]["x"]+bullets[id]["vx"]*(server_clock-last_update)*bullet_speed
		bullets[id]["y"] = bullets[id]["y"]+bullets[id]["vy"]*(server_clock-last_update)*bullet_speed

	last_update = server_clock

@socketio.on('request_frame')
def handle_client_request(id):
	
	players_update(last_update)
	emit('update_pos',{"x" : players[id]["x"],"y" : players[id]["y"] } )
	emit('update',{"players" : players,"bullets" : bullets} )

if __name__ == '__main__':
	app.debug = True
	socketio.run(app, host='localhost', port=5000)
