from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, send, emit

import random
import numpy as np
import time as time
from math import *
from generate_map import *

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

# returning a random color
def getRandomColor():
  letters = '0123456789ABCDEF'
  color = '#'
  for i in range(6):
    color += letters[int(np.floor(random.random()*16))]
  return color

# defining the /game page by the file client.html
@app.route('/game')
def index():
    return render_template('client.html')

# definign the login page by the file login.html
@app.route('/login', methods=['GET','POST'])
def login():
    # session is a cookie saving the pseudo of the player
    # if pseudo is known, the player is redirected to the game
    if 'pseudo' in session:
       return redirect('/game')

    # the pseudo is not known
    else:
        # the formulary of login page has been sent
        if request.method == 'POST':
            # the player want to save his session for a month
            if(str(request.form['result']) == 'Oui'):
                session['pseudo'] = str(request.form['ps'])
                session.permanent = True
            # the player doesn't want to save his session
            else:
                print("test")
                session['pseudo'] = str(request.form['ps'])
            #redirecting the player to the game
            return redirect('/game')

        # the formulary has not been sent, we return the login page
        else:
            return render_template('login.html')

    # if request.method == 'POST':
    #     session['pseudo'] = str(request.form['ps'])
    #     return redirect('/game')
    # else:
    #     return render_template('login.html')

@socketio.on('new_connection')
def handle_new_connection():
	print("Un joueur connecte")
	id = int(time.clock()*10**5)
	players[id] = {"x" :Xstart, "y" : Ystart, "vx" : 0,"vy" : 0, "r" : bigballRadius, "color" : getRandomColor(), "pseudo" : session['pseudo'], "score" : 0}
	emit('authentification', id )
	print("Fin transfert map")
    	file_p.write(format(time.clock(), '.10f')+",")
    	file_p.write(str(len(players))+"\n")



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

# defining the /end_game page
@app.route('/end_game', methods=['GET','POST'])
def players_dead():
    # if the player click on the button then he his redirected to the game
    if request.method == 'POST':
        return redirect('/game')
    # the player has not clicked
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

    	file.write(format(server_clock, '.10f')+",")
        file.write(format(time.clock() - server_clock, '.10f')+"\n")
        file.flush()


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

# defining the application
if __name__ == '__main__':

	file = open('activity_log.txt','w')
    	file.seek(0)
    	file.truncate()

    	file_p = open('players_connected.txt','w')
    	file_p.seek(0)
    	file_p.truncate()

	app.debug = True
	print("map size : ", map_width, map_height, " : ", map_width*map_height )
	socketio.run(app, host='127.0.0.1', port=5000)
