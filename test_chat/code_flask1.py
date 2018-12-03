from flask import Flask, render_template
from flask_socketio import SocketIO
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('login.html')

users = []
messages_sent = {}


@socketio.on('login')
def handle_message(login):
    print('user '+login+ ' connected ! ')
    users.append(login)
    messages_sent[login] = 0
    
@socketio.on('message')
def handle_message(login, msg):
    messages_sent[login] += 1
    print('new message by ' + login + " : " + msg )
    
if __name__ == '__main__':
    socketio.run(app)


