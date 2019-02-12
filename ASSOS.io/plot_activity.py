
import matplotlib.pyplot as plt
import time as time
from math import *

def mean(x):
    res = 0
    for e in x:
        res += pow(e,2)
    return sqrt(res/len(x))
def kde (x,bw):
    n = len(x)
    res = [0]*n
    for k in range(n):
        res[k] = mean(x[k:min(n,k+bw)])
    return res

times = []
proc = []

times_p = []
players = []

figp = plt.gcf()
figp.show()
figp.canvas.draw()

bw = 50
file =  open('activity_log.txt', 'r+')
file_p = open('players_connected.txt',"r+")
size = 1200

while(True):
    new_data = file.readlines()
    # file.seek(0)
    # file.truncate()
    for d in new_data:
        l = d.rstrip().split(",")
        if len(l) > 1 :
            times.append(float(l[0]))
            proc.append(float(l[1]))

    plt.clf()
    plt.plot(times[-size:-bw],kde(proc[-size:-bw],bw),color = "r")
    plt.xlim(times[len(times)-size])
    plt.ylim(0,0.3)

    new_p_data = file_p.readlines()
    l=[]
    for d in new_p_data:
        l = d.rstrip().split(",")
        if len(l) > 1 :
            times_p.append(float(l[0]))
            players.append(int(l[1]))
    plt.plot(times_p,players,color = "blue")
    figp.canvas.draw()


    time.sleep(0.05)
