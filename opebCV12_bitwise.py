#program launches the rpi cam with jetson nano
#learning to use bitwise operators and masks.

import cv2
import numpy as np

print(cv2.__version__)

#Setting up the camera
dispW=640
dispH=480
flip=0

img1 = np.zeros((480,640,1), np.uint8) #setting up grayscale matrix
img1[0:480,0:320] = [255]   #white on the left, black on the right

img2 = np.zeros((480,640,1), np.uint8)
img2[190:290, 270:370] = [255]  #create box in middle

bitAnd = cv2.bitwise_and(img1, img2)
bitOr = cv2.bitwise_or(img1, img2)
bitXor = cv2.bitwise_xor(img1, img2)

#Start camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)

#Read camera until q key is pressed
while True:
    ret, frame = cam.read()

    cv2.imshow('img1', img1)
    cv2.moveWindow('img1', 0, 520)
    cv2.imshow('img2', img2)
    cv2.moveWindow('img2', 705, 520)
    cv2.imshow('AND', bitAnd)
    cv2.moveWindow('AND', 705, 0)
    cv2.imshow('OR', bitOr)
    cv2.moveWindow('OR', 1350, 0)
    cv2.imshow('XOR', bitXor)
    cv2.moveWindow('XOR', 1350, 520)

    frame = cv2.bitwise_and(frame,frame,mask=bitXor)
    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 0)
    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()