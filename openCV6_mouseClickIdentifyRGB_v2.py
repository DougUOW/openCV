#program launches the rpi cam with jetson nano.
#program will identfy location of mouse button clicks and also can be used as a colour picker.
#Clicking left mouse button will place a dot on the video image and also the point location.
#Clicking the right mouse button will identify the RGB values at that point, then open another window
#that shows the colour selected and the appropriate RGB values.

#this is a modified version that just prints the RGB values in the terminal window
#need to get HSV Values!

import cv2
import numpy as np

print(cv2.__version__)

#When the mouse click event is dtected, this function is called.
def click(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:

        blue = frame[y,x,0]
        green = frame[y,x,1]
        red = frame[y,x,2]
        hue = frame_hsv[y,x,0]
        sat = frame_hsv[y,x,1]
        value = frame_hsv[y,x,2]
        print("BGR Values: ", blue,green,red)
        print("HSV Values: ", hue,sat,value)

#Setting up the camera
dispW=640
dispH=480
flip=0

cv2.namedWindow('frame_hsv')
cv2.setMouseCallback('frame_hsv', click)

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)

#Read camera until q key is pressed
while True:
    ret, frame = cam.read()
    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 0)

    #convert original image (frame) from BGR 2 HSV
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('frame_hsv', frame_hsv)
    cv2.moveWindow('frame_hsv', 710, 0)

    keyEvent = cv2.waitKey(1)
    if keyEvent == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()