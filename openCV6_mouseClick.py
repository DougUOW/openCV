#program launches the rpi cam with jetson nano.
#program will identfy location of mouse button clicks

import cv2

print(cv2.__version__)

evt = -1
coord = []

def click(event, x, y, flags, params):
    global pnt
    global evt
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Mouse event was:   ', event)
        print(x,',',y)
        pnt = (x,y)
        coord.append(pnt)
        print(coord)
        evt = event

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