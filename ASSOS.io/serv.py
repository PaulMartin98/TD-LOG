from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, send, emit

import random
import numpy as np
import time as time
from math import *
from generate_map import *
from threading import Thread

map, map_width, map_height = get_map("../maps/test_img2.png")
app = Flask(__name__)

app.config['SECRET_KEY'] = 'scret'
width, height = 1000, 1000
socketio = SocketIO(app)

Xstart , Ystart = 0, 0
speed = 3
bullet_speed = 8
players = {}
bullets = {}

bigballRadius = 15;
smallballRadius = 3;

server_clock = time.clock()
last_update = server_clock
refreshing_time = 1/120
last_broadcast = time.clock()

def getRandomColor():
  letters = '0123456789ABCDEF'
  color = '#'
  for i in range(6):
    color += letters[int(np.floor(random.random()*16))]
  return color

@app.route('/game')
def index():
    return render_template('client.html')

@app.route('/login', methods=['GET','POST'])
def login():
    #if 'pseudo' in session:
    #    return redirect('/game')
    # else:
    #     if request.method == 'POST':
    #         if(str(request.form['sess']) == 'on'):
    #             session['pseudo'] = str(request.form['ps'])
    #             session.permanent = True
    #         else:
    #             session['pseudo'] = str(request.form['ps'])
    #         return redirect('/game')
    #     return render_template('login.html')

    if request.method == 'POST':
        session['pseudo'] = str(request.form['ps'])
        return redirect('/game')
    else:
        return render_template('login.html')

@socketio.on('new_connection')
def handle_new_connection():
	print("Un joueur connecte")
	id = int(time.clock()*10**5)
	players[id] = {"x" :Xstart, "y" : Ystart, "vx" : 0,"vy" : 0, "r" : bigballRadius, "color" : getRandomColor(), "pseudo" : session['pseudo'], "score" : 0}
	emit('authentification', id )
	print("Fin transfert map")



@socketio.on('client_speed_update')
def handle_move(id,vx,vy):
	players[id]['vx'] = vx
	players[id]['vy'] = vy


@socketio.on('client_shoot')
def handle_shoot(id,vx,vy):
	global shoot
	shoot = True
	bullet_id = random.randint(100, 200)
	bullets[bullet_id] = { "x" : players[id]["x"],
						   "y" : players[id]["y"],
						   "vx" : vx ,
						   "vy" : vy ,
						   "color" : players[id]["color"],
						   "player_id" : id}

@socketio.on('logout')
def handle_logout():
    return redirect('/end_game')

@app.route('/end_game', methods=['GET','POST'])
def players_dead():
    if request.method == 'POST':
        return redirect('/game')
    else:
        return render_template('end_game.html')

def players_update():
	global server_clock, last_update
	server_clock = time.clock()
	topopbul = []
	topopplay = []
	for id in players:
		new_x = players[id]["x"]+players[id]["vx"]*(server_clock-last_update)*speed
		new_y = players[id]["y"]+players[id]["vy"]*(server_clock-last_update)*speed
		if  (0 < new_y < map_height) and (0 < new_x < map_width) and (map[int(new_y)][int(new_x)] == False) :
			players[id]["x"] = new_x
			players[id]["y"] = new_y
		#if players[id]["r"]<6:
		#	topopplay.append(id)

	for id in bullets:
		new_x = bullets[id]["x"]+bullets[id]["vx"]*(server_clock-last_update)*bullet_speed
		new_y = bullets[id]["y"]+bullets[id]["vy"]*(server_clock-last_update)*bullet_speed
		if  (0 < new_y < map_height) and (0 < new_x < map_width) and (map[int(new_y)][int(new_x)] == False) :
			bullets[id]["x"] = new_x
			bullets[id]["y"] = new_y
		else :
			topopbul.append(id)
		for idp in players:
			if (players[idp]["color"] != bullets[id]["color"] and (players[idp]["x"]-bullets[id]["x"])**2 + (players[idp]["y"]-bullets[id]["y"])**2 <= (players[idp]["r"] + smallballRadius)**2):
				players[idp]["r"] -= 4
				topopbul.append(id)
                if players[idp]["r"]<6:
                    topopplay.append(idp)
                    players[bullets[id]["player_id"]]["score"] +=1

	for id in topopbul:
		bullets.pop(id, None)
	for id in topopplay:
		players.pop(id,None)
		socketio.emit('dead', id, broadcast = True )
		#return redirect('/end_game')
	last_update = server_clock


@socketio.on('rendering')
def handle_rendering():
	print("le temps est ")


@socketio.on('request_frame')
def handle_request_frame():
	global last_broadcast
	if time.clock() - last_broadcast > refreshing_time :
		players_update()
		socketio.emit('update', {"players" : players, "bullets" : bullets}, broadcast= True)
		last_broadcast = time.clock()

if __name__ == '__main__':
	app.debug = False
	print("map size : ", map_width, map_height, " : ", map_width*map_height )
	socketio.run(app, host='127.0.0.1', port=5000)
