#program launches the rpi cam with jetson nano
#aqdding drawings on frames/images

import cv2

print(cv2.__version__)

#Setting up the camera
dispW=640
dispH=480
flip=0
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(camSet)

#Read camera until q key is pressed
while True:
    ret, frame = cam.read()
    frame = cv2.rectangle(frame, (140,100), (180,140), (255,0,0), 4)
    frame = cv2.circle(frame, (320,240), 50, (0,255,0), 2)
    fnt = cv2.FONT_HERSHEY_DUPLEX
    frame = cv2.putText(frame, 'My First Text', (400,300), fnt, 1, (0,0,255), 1)
    frame = cv2.line(frame, (140, 350), (250,400), (0,0,0), 5)
    frame = cv2.arrowedLine(frame, (500,100), (630,100), (255,255,255), 3)
    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 0)
    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()