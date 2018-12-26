

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import random 
import numpy as np
import time as time
from math import *

app = Flask(__name__)

app.config['SECRET-KEY'] = 'scret'
width, height = 1000, 1000
dt = 0.005
socketio = SocketIO(app)

Xstart , Ystart = 200, 200
speed = 0.005
bullet_speed = 0.01
players = {}
bullets = {}

bigballRadius = 10;
smallballRadius = 3;

server_clock = time.clock()
last_update = server_clock


def getRandomColor():
  letters = '0123456789ABCDEF'
  color = '#'
  for i in range(6):
    color += letters[int(np.floor(random.random()*16))]
  return color

@app.route('/')
def index():
	return render_template('client.html')

@socketio.on('new_connection')
def handle_new_connection():
	#print("new player connected")
	id = int(time.time())
	players[id] = {"x" :Xstart, "y" : Ystart, "vx" : 0,"vy" : 0, "color" : getRandomColor(), "r" : 10}
	emit('authentification',id)

@socketio.on('client_speed_update')
def handle_move(id,vx,vy):
	# print('update',vx,vy)
	players[id]['vx'] = vx
	players[id]['vy'] = vy
	#print(players)
@socketio.on('client_shoot')
def handle_shoot(id,vx,vy):
	print('shoot !', id)
	bullet_id = random.randint(100, 200)
	bullets[bullet_id] = { "x" : players[id]["x"],
						   "y" : players[id]["y"], 
						   "vx" : vx ,
						   "vy" : vy ,
						   "color" : players[id]["color"]}

@socketio.on('collision_test')
def handle_collision(id_bullets):
	for id_players in players:
		print(players[id_players]["r"])
		if (players[id_players]["color"] != bullets[id_bullets]["color"] and (players[id_players]["x"]-bullets[id_bullets]["x"])**2 + (players[id_players]["y"]-bullets[id_bullets]["y"])**2 <= (players[id_players]["r"] + smallballRadius)**2):
			players[id_players]["r"] += 5 
			bullets.pop(id_bullets, None)
	 

def players_update(last_update):
	server_clock = time.clock()
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
	emit('update_pos', {"x" : players[id]["x"], "y" : players[id]["y"] })
	emit('update', {"players" : players, "bullets" : bullets})

if __name__ == '__main__':
	app.debug = True
	socketio.run(app, host='localhost', port=5000)
