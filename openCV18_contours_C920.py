#Exactly the same as openCv18_contours, exept uses the logitch c920

import cv2
import numpy as np  #numpy is the mathematical library that works with arrays.

#Dummy function as createTrackbar function requires it.
def nothing(x):
    pass

#Setting up the camera
#dispW=640
#dispH=480
#flip=0
#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#cam = cv2.VideoCapture(camSet)
cam = cv2.VideoCapture(1)
cam.set(3,640)
cam.set(4,480)

#Setup trackbars that allow us to quickly change HSV values
cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars', 1320, 0)
cv2.createTrackbar('hueLow', 'Trackbars', 165, 179, nothing)
cv2.createTrackbar('hueHigh', 'Trackbars', 179, 179, nothing)

cv2.createTrackbar('hueLow2', 'Trackbars', 0, 179, nothing)
cv2.createTrackbar('hueHigh2', 'Trackbars', 3, 179, nothing)

cv2.createTrackbar('satLow', 'Trackbars', 120, 255, nothing)
cv2.createTrackbar('satHigh', 'Trackbars', 255, 255, nothing)

cv2.createTrackbar('valueLow', 'Trackbars', 120, 255, nothing)
cv2.createTrackbar('valueHigh', 'Trackbars', 255, 255, nothing)

while True:
    ret, frame = cam.read()
    #convert original image (frame) from BGR 2 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Get values from Trackbars
    hueLow = cv2.getTrackbarPos('hueLow', 'Trackbars')
    hueHigh = cv2.getTrackbarPos('hueHigh', 'Trackbars')
    hueLow2 = cv2.getTrackbarPos('hueLow2', 'Trackbars')
    hueHigh2 = cv2.getTrackbarPos('hueHigh2', 'Trackbars')
    satLow = cv2.getTrackbarPos('satLow', 'Trackbars')
    satHigh = cv2.getTrackbarPos('satHigh', 'Trackbars')
    valueLow = cv2.getTrackbarPos('valueLow', 'Trackbars')
    valueHigh = cv2.getTrackbarPos('valueHigh', 'Trackbars')
    #Create arrays to store HSV Low High values
    lower_bound = np.array([hueLow, satLow, valueLow])
    upper_bound = np.array([hueHigh, satHigh, valueHigh])
    lower_bound2 = np.array([hueLow2, satLow, valueLow])
    upper_bound2 = np.array([hueHigh2, satHigh, valueHigh])
    
    #Create FOREGROUND MASK. Fuction only returns 1's and 0's. 1 for any pixel that
    #is in range, 0 for any vale out of range
    FGmask = cv2.inRange(hsv, lower_bound, upper_bound)
    FGmask2 = cv2.inRange(hsv, lower_bound2, upper_bound2)
    FGmaskcomp = cv2.add(FGmask,FGmask2)
    #Show the FGMaskcom
    cv2.imshow('FGmaskcomp', FGmaskcomp)
    cv2.moveWindow('FGmaskcomp', 0, 410)

    contours,_ = cv2.findContours(FGmaskcomp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    #cv2.drawContours(frame, contours, 0, (255,0,0), 3)

    #sometimes we may need to track multiple objects. This for loop does this
    #Will also draw a rectangle around selected object, and a crosshair, based on the centre
    #of the object
    for cnt in contours:
        area = cv2.contourArea(cnt)
        (x,y,w,h) = cv2.boundingRect(cnt)
        if area >= 500:
            #cv2.drawContours(frame, [cnt], 0, (255,0,0), 3)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3)
            cv2.circle(frame, (int(x+w/2), int(y+h/2)), 5, (0,255,0), -1)
            cv2.line(frame, (0, int(y+h/2)), (640, int(y+h/2)), (0,255,0), 1)
            cv2.line(frame, (int(x+w/2), 0), (int(x+w/2), 480), (0,255,0), 1)
   
    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 0)

    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()