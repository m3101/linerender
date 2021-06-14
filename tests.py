import numpy as np
from numpy.lib import math
import projections as pj
import images as im
from cv2 import cv2

cv2.namedWindow("FUNCIONA!",cv2.WINDOW_KEEPRATIO)

#A camera at 1 1 1
position = np.array([0,0,-70])
#Looking at our origin
rotation = -position

cam = pj.Camera(position,rotation,0,1)

pts = np.array([
    [-10,10,-10,1],[10,10,-10,1],
    [-10,-10,-10,1],[10,-10,-10,1],
    [-10,10,10,1],[10,10,10,1],
    [-10,-10,10,1],[10,-10,10,1],
    [0,0,0,1]
])
lns = [
    [0,1],[0,2],[0,4],[3,1],[3,2],[3,7],
    [2,6],[1,5],
    [4,5],[4,6],[7,6],[7,5]

]

plano = np.array(
    [
        [20,-10,20,1],[-20,-10,20,1],
        [-20,-10,-20,1],[20,-10,-20,1],
    ]
)
plinhas = [[0,1],[1,2],[2,3],[3,0]]

pontoquique = np.array([[5,40,5,1]])

#Main loop
fd=500
roda_roda_vira = False
ang = 0.01
roda = np.array([
    [math.cos(ang),0,-math.sin(ang)],
    [0,1,0],
    [math.sin(ang),0,math.cos(ang)]
])

vy = 0
def simula():
    global vy
    pontoquique[0][1]+=vy
    if pontoquique[0][1]<-10:
        print("QUIQUE")
        print(vy)
        vy = (vy*0.9)
        vy = vy * math.copysign(1,vy)
        print(vy)
        diff = -10 - pontoquique[0][1]
    vy-=0.0981

while(True):
    rotation = -position
    cam.calibrate(position,rotation,0,fd)
    img = im.image(cam,pts,lns)
    img = im.image(cam,plano,plinhas,base=img)
    img = im.image(cam,pontoquique,[],base=img)
    cv2.putText(img,f"{vy}",(20,20),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
    cv2.imshow("FUNCIONA!",img)
    if roda_roda_vira:
        position = np.dot(position,roda)
    simula()
    key = cv2.waitKey(1)&0xFF
    if key == ord('w'):
        position[2]+=1
    elif key == ord('a'):
        position[0]-=1
    elif key == ord('s'):
        position[2]-=1
    elif key == ord('d'):
        position[0]+=1
    elif key == ord('r'):
        position[1]-=1
    elif key == ord('f'):
        position[1]+=1
    elif key == ord('z'):
        fd+=1
    elif key == ord('x'):
        fd-=1
    elif key == ord('g'):
        roda_roda_vira = not roda_roda_vira
    elif key == ord('q'):
        break