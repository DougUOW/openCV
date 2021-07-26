#program launches the rpi cam with jetson nano

import cv2

print(cv2.__version__)

#Setting up the camera
dispW=640
dispH=480
flip=0
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(camSet)
#To read vid from file, comment out line below, then comment all outVid lines.
#cam = cv2.VideoCapture('videos/myCam.avi')
outVid = cv2.VideoWriter('videos/myCam.avi', cv2.VideoWriter_fourcc(*'XVID'), 21, (dispW,dispH))

#Read camera until q key is pressed
while True:
    ret, frame = cam.read()
    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 0)
    outVid.write(frame)
    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
outVid.release()
cv2.destroyAllWindows()