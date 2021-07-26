#program launches the rpi cam with jetson nano

import cv2

print(cv2.__version__)

def nothing():
    pass

#Setting up the camera
dispW=640
dispH=480
flip=0

#paramters for the bouncing box
boxWidth = 80
boxHeight = 60

boundaryBottom = int(dispH - (boxHeight))
boundaryRight = int(dispW - (boxWidth))

locationHeight = 0
locationWidth =0

dWidth= 2  #change in width
dHeight = 2 #change in height

i = 0
flagHeight = 0
flagWidth = 0

#CREATE BACKGROUND MASK
#load cv.jpg image, 
cvLogo = cv2.imread('pl.jpg')
cvLogo = cv2.resize(cvLogo,(80,60))
cv2.imshow('1.Original Logo', cvLogo)
cv2.moveWindow('1.Original Logo', 0,530)
#convert cvLogo to gray
cvLogoGray = cv2.cvtColor(cvLogo, cv2.COLOR_BGR2GRAY)
cv2.imshow('2.Make Gray Scale', cvLogoGray)
cv2.moveWindow('2.Make Gray Scale', 150, 530)
#setup BG Mask threshold. Make all grey tones black.
_, BGMask = cv2.threshold(cvLogoGray, 225, 255, cv2.THRESH_BINARY) #_ = unused variable
cv2.imshow('3.Make BG Mask', BGMask)
cv2.moveWindow('3.Make BG Mask', 235, 530 )

#CREATE FOREGROUND MASK
#create foreground mask, by inverting BGMask
FGMask = cv2.bitwise_not(BGMask)
cv2.imshow('4.Make FG Mask', FGMask)
cv2.moveWindow('4.Make FG Mask',335, 530)
#create foreground
FG=cv2.bitwise_and(cvLogo,cvLogo,mask=FGMask)
cv2.imshow('5.FG= cvLogo & FGMask', FG)
cv2.moveWindow('5.FG= cvLogo & FGMask', 435, 530)

#Setup Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)

#Read camera until q key is pressed
while True:
    ret, frame = cam.read()
    #roi = frame[100:160, 200:280].copy()
    roi = frame[locationHeight:(locationHeight+boxHeight), locationWidth:(locationWidth+boxWidth)].copy()

    BG = cv2.bitwise_and(roi,roi,mask=BGMask)
    cv2.imshow('6.roi',BG)
    cv2.moveWindow('6.roi', 535, 530)

    compImage = cv2.add(BG,FG)
    cv2.imshow('7.compImage= BG + FG', compImage)
    cv2.moveWindow('7.compImage= BG + FG', 635, 530)

    #insert compImage into the frame matrix
    frame[locationHeight:(locationHeight+boxHeight), locationWidth:(locationWidth+boxWidth)] = compImage

    cv2.imshow('piCam',frame)
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