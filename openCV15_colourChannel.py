#program launches the rpi cam with jetson nano

import cv2
import numpy as np

print(cv2.__version__)

#Setting up the camera
dispW=640
dispH=480
flip=0
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(camSet)

#Read camera until q key is pressed

#make a matrix, which we will use as an image
blank = np.zeros([480,640,1],np.uint8)
#make corner square grey
#blank[0:240, 0:320]=125

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #show matrix properties of frame
    #print (frame.shape)
    #print (gray.shape)
    #print (gray.size)
    #print (frame.size)
    #print green value at certain pixel
    print (frame[50,45,1])

    #show individual colours in image
    #blue = cv2.split(frame)[0]
    #green = cv2.split(frame)[1]
    #red = cv2.split(frame)[2]
    b,g,r = cv2.split(frame)

    blue = cv2.merge((b, blank, blank))
    green = cv2.merge((blank, g, blank))
    red = cv2.merge((blank, blank, r))


    #show images
    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 0) 
    cv2.imshow('blue',blue)
    cv2.moveWindow('blue', 705, 0)
    cv2.imshow('green',green)
    cv2.moveWindow('green', 0, 520)
    cv2.imshow('red',red)
    cv2.moveWindow('red', 705, 520)

    cv2.imshow('blank', blank)
    cv2.moveWindow('blank', 1380,0)

    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()