import numpy as np
from numpy.lib import math
import projections as pj
import images as im
from cv2 import cv2
import pynput

mouse = pynput.mouse.Controller()
keys = "wasd"
walkeys = {k:False for k in keys}

def keypress(key):
    walkeys[str(key)[1]] = True
def keyrelease(key):
    walkeys[str(key)[1]] = False
klistener = pynput.keyboard.Listener(
    on_press=keypress,
    on_release=keyrelease
)
klistener.start()

cv2.namedWindow("FUNCIONA!",cv2.WINDOW_KEEPRATIO)

#A camera at 1 1 1
position = np.array([0,0,-70])
#Looking at our origin
rotation = -position/70

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
right = np.array([
    [math.cos(ang),0,-math.sin(ang)],
    [0,1,0],
    [math.sin(ang),0,math.cos(ang)]
])
left = np.linalg.inv(right)

ang = 0.01
up = np.array([
    [1,0,0],
    [0,math.cos(ang),-math.sin(ang)],
    [0,math.sin(ang),math.cos(ang)]
])
down = np.linalg.inv(up)

vy = 0
def simula():
    global vy
    pontoquique[0][1]+=vy
    if pontoquique[0][1]<-10:
        vy = (vy*0.9)
        vy = vy * math.copysign(1,vy)
        diff = -10 - pontoquique[0][1]
    vy-=0.0981

def postprocess(img,trh=50):
    s = (img[:,:,0].astype(float)+img[:,:,1].astype(float)+img[:,:,2].astype(float))/3
    b = np.zeros(img.shape,dtype=np.float32)
    b[s>trh] = img[s>trh]
    b = cv2.blur(b,(4,4))
    b = b + img
    b[b>255] = 255
    return b.astype(np.uint8)
cm = False
def control_mouse(r=500,f=0.1):
    global mouse,rotation
    dx = r - mouse.position[0]
    dy = r - mouse.position[1]
    br = rotation.copy()
    if dx>0:
        rotation = np.dot(rotation,left*dx/f)
    elif dx!=0:
        print(dx)
        rotation = np.dot(rotation,-right*dx/f)
    if dy>0:
        rotation = np.dot(rotation,up*dy/f)
    elif dy!=0:
        rotation = np.dot(rotation,-down*dy/f)
    if (rotation==0).sum()==3:
        rotation = br
    print(rotation)
    rotation = rotation/np.linalg.norm(rotation)
    mouse.position = (r,r)
def control_kb():
    global walkeys,position,rotation
    perp = np.cross(rotation,[0,1,0])
    if walkeys['w']:
        position = position+rotation
    elif walkeys['s']:
        position = position-rotation
    if walkeys["a"]:
        position = position+perp
    elif walkeys["d"]:
        position = position-perp
while(True):
    if not cm:
        pass
        #rotation = -position
    cam.calibrate(position,rotation,0,fd)
    img = im.image(cam,pts,lns)
    img = im.image(cam,plano,plinhas,base=img)
    img = im.image(cam,pontoquique,[],base=img)
    cv2.putText(img,f"{vy}",(20,20),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
    img = postprocess(img)
    cv2.imshow("FUNCIONA!",img)
    if roda_roda_vira:
        rotation = np.dot(rotation,down)
    simula()
    if cm:
        control_mouse()
    control_kb()
    key = cv2.waitKey(1)&0xFF
    if key == ord('z'):
        fd+=1
    elif key == ord('x'):
        fd-=1
    elif key == ord('g'):
        roda_roda_vira = not roda_roda_vira
    elif key == ord('m'):
        mouse.position = (10,10)
        cm = not cm
    elif key == ord('q'):
        break