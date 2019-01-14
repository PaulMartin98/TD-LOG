

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import random
import numpy as np
import time as time
from math import *
from generate_map import *
from threading import Thread
# from flask_apscheduler import APScheduler




map, map_width, map_height = get_map("../maps/test_img2.png")
app = Flask(__name__)

app.config['SECRET-KEY'] = 'scret'
width, height = 1000, 1000
dt = 0.005
socketio = SocketIO(app)

Xstart , Ystart = 0, 0
speed = 5
bullet_speed = 15
players = {}
bullets = {}

bigballRadius = 15;
smallballRadius = 3;

server_clock = time.clock()
last_update = server_clock
refreshing_time = 0.0015
last_broadcast = time.clock()
# frames = 0

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

	print("new player connected")
	id = int(time.clock()*10**5)
	print(id)
	players[id] = {"x" :Xstart, "y" : Ystart, "vx" : 0,"vy" : 0, "r" : bigballRadius, "color" : getRandomColor() }
	team = 0
	emit('authentification',
	{"id" : id, "team" : team, "map" : map, "map_width" : map_width, "map_height" : map_height, "color" : getRandomColor(), "r" : bigballRadius} )


@socketio.on('client_speed_update')
def handle_move(id,vx,vy):
	# print('update',id,vx,vy)
	players[id]['vx'] = vx
	players[id]['vy'] = vy
@socketio.on('client_shoot')
def handle_shoot(id,vx,vy):
	# print('shoot !', id)
	global shoot
	shoot = True
	bullet_id = random.randint(100, 200)
	bullets[bullet_id] = { "x" : players[id]["x"],
						   "y" : players[id]["y"],
						   "vx" : vx ,
						   "vy" : vy ,
						   "color" : players[id]["color"],
						   "player_id" : id}

def players_update():
	global server_clock, last_update
	server_clock = time.clock()
	topopbul = []
	topopplay = []
	for id in players:
		new_x = players[id]["x"]+players[id]["vx"]*(server_clock-last_update)*speed
		new_y = players[id]["y"]+players[id]["vy"]*(server_clock-last_update)*speed
		if  (0 < new_y < map_height) and (0 < new_x < map_width) and (map[int(new_y) + map_height*int(new_x)] == 0) :
			players[id]["x"] = new_x
			players[id]["y"] = new_y
		if players[id]["r"]<6:
			topopplay.append(id)

	for id in bullets:
		new_x = bullets[id]["x"]+bullets[id]["vx"]*(server_clock-last_update)*bullet_speed
		new_y = bullets[id]["y"]+bullets[id]["vy"]*(server_clock-last_update)*bullet_speed
		if  (0 < new_y < map_height) and (0 < new_x < map_width) and (map[int(new_y) + map_height*int(new_x)] == 0) :
			bullets[id]["x"] = new_x
			bullets[id]["y"] = new_y
		else :
			topopbul.append(id)
		for idp in players:
			if (players[idp]["color"] != bullets[id]["color"] and (players[idp]["x"]-bullets[id]["x"])**2 + (players[idp]["y"]-bullets[id]["y"])**2 <= (players[idp]["r"] + smallballRadius)**2):
				players[idp]["r"] -= 4
				topopbul.append(id)



	for id in topopbul:
		bullets.pop(id, None)
	for id in topopplay:
		players.pop(id,None)
        	socketio.emit('dead',id,broadcast = True )

	last_update = server_clock

@socketio.on('request_frame')
def handle_request_frame():
	global last_broadcast
	if time.clock() - last_broadcast > refreshing_time :
		players_update()
		socketio.emit('update', {"players" : players, "bullets" : bullets}, broadcast= True)
		last_broadcast = time.clock()

# @socketio.on('collision_test')
# def handle_collision(id_bullets):
# 	for id_players in players:
# 		# print(players[id_players]["r"])
# 		if (players[id_players]["color"] != bullets[id_bullets]["color"] and (players[id_players]["x"]-bullets[id_bullets]["x"])**2 + (players[id_players]["y"]-bullets[id_bullets]["y"])**2 <= (players[id_players]["r"] + smallballRadius)**2):
# 			players[id_players]["r"] += 5
# 			bullets.pop(id_bullets, None)

if __name__ == '__main__':


	app.debug = True
	print("map size : ", map_width, map_height, " : ", map_width*map_height )

	socketio.run(app, host='0.0.0.0', port=5000)
