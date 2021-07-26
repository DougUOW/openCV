#program launches the rpi cam with jetson nano.
#program will identfy location of mouse button clicks and also can be used as a colour picker.
#Clicking left mouse button will place a dot on the video image and also the point location.
#Clicking the right mouse button will identify the RGB values at that point, then open another window
#that shows the colour selected and the appropriate RGB values.

import cv2
import numpy as np

print(cv2.__version__)

evt = -1
coord = []
img = np.zeros((250,250,3), np.uint8)

def click(event, x, y, flags, params):
    global pnt
    global evt
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Mouse event was:   ', event)
        print(x,',',y)
        pnt = (x,y)
        coord.append(pnt)
        #print(coord)
        evt = event
    if event == cv2.EVENT_RBUTTONDOWN:
        print (x,y)
        blue = frame[y,x,0]
        green = frame[y,x,1]
        red = frame[y,x,2]
        print(blue,green,red)
        colorString = str(blue)+','+str(green)+','+str(red)
        img[:] = [blue,green,red]
        fnt=cv2.FONT_HERSHEY_PLAIN
        r = 255-int(red)
        g = 255-int(green)
        b = 255-int(blue)
        tp = (b,g,r)
        cv2.putText(img, colorString, (10,25), fnt, 1, tp, 2)
        cv2.imshow('myColor', img)

#Setting up the camera
dispW=640
dispH=480
flip=0

cv2.namedWindow('piCam')
cv2.setMouseCallback('piCam', click)

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)

#Read camera until q key is pressed
while True:
    ret, frame = cam.read()
    for pnts in coord:
        cv2.circle(frame, pnts, 5, (0,0,255), -1)
        font = cv2.FONT_HERSHEY_PLAIN
        myStr = str(pnts)
        cv2.putText(frame, myStr, pnts, font, 1, (255,0,0), 2)
    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 0)
    keyEvent = cv2.waitKey(1)
    if keyEvent == ord('c'):
        coord = []
    if keyEvent == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()