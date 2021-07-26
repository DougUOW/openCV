#program launches the rpi cam with jetson nano
#bouncing ball exercise

import cv2

print(cv2.__version__)

#Setting up the camera
dispW=640
dispH=480
flip=0
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(camSet)

#Read camera until q key is pressed
boxWidth = 100
boxHeight = 100

boundaryBottom = int(dispH - (boxHeight))
boundaryRight = int(dispW - (boxWidth))

locationHeight = 0
locationWidth =0

dWidth= 2  #change in width
dHeight = 2 #change in height

i = 0
flagHeight = 0
flagWidth = 0

while True:
    ret, frame = cam.read()     #read individual frames from camera
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     #convert frame to grayscale
    frameGray = cv2.cvtColor(frameGray, cv2.COLOR_GRAY2BGR) #Convert graysacale to colour. Ensures matching data types
    roi = frame[locationHeight:(locationHeight+boxHeight), locationWidth:(locationWidth+boxWidth)].copy()   #grab roi, depending upon bouncing box
    frameGray[locationHeight:(locationHeight+boxHeight), locationWidth:(locationWidth+boxWidth)] = roi  #insert roi into grayscale image
    frameGray = cv2.rectangle(frameGray, (locationWidth,locationHeight), ((locationWidth+boxWidth),(locationHeight+boxHeight)), (0,0,255), 2)

    cv2.imshow('piCam',frameGray)
    cv2.moveWindow('piCam', 0, 0)

    if flagWidth == 0: #move right
        locationWidth = locationWidth + dWidth
        if locationWidth > boundaryRight:
            locationWidth = boundaryRight
            flagWidth = 1
    if flagWidth == 1: #move left
        locationWidth = locationWidth - dWidth
        if locationWidth < 0:
            locationWidth = 0
            flagWidth = 0  

    if flagHeight == 0: #move down
        locationHeight = locationHeight + dHeight
        if locationHeight > boundaryBottom:
            locationHeight = boundaryBottom
            flagHeight = 1
    if flagHeight == 1: #move up
        locationHeight = locationHeight - dHeight
        if locationHeight < 0:
            locationHeight = 0
            flagHeight = 0  

    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()