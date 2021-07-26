#program launches the rpi cam with jetson nano

import cv2

print(cv2.__version__)

def nothing():
    pass

cv2.namedWindow('blended')
cv2.createTrackbar('blendValue', 'blended', 50, 100, nothing)

#Setting up the camera
dispW=320
dispH=240
flip=0

#load cv.jpg image, convert to gray
cvLogo = cv2.imread('cv.jpg')
cvLogo = cv2.resize(cvLogo,(320,240))
cvLogoGray = cv2.cvtColor(cvLogo, cv2.COLOR_BGR2GRAY)
cv2.imshow('cv Logo Gray', cvLogoGray)
cv2.moveWindow('cv Logo Gray', 0, 350)

#setup threshold
_, BGMask = cv2.threshold(cvLogoGray, 225, 255, cv2.THRESH_BINARY) #_ = unused variable
cv2.imshow('BG Mask', BGMask)
cv2.moveWindow('BG Mask', 385, 100 )

#create foreground mask
FGMask = cv2.bitwise_not(BGMask)
cv2.imshow('FG Mask', FGMask)
cv2.moveWindow('FG Mask', 385, 350)
FG=cv2.bitwise_and(cvLogo,cvLogo,mask=FGMask)
cv2.imshow('FG', FG)
cv2.moveWindow('FG', 703, 350)

#Setup Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)

#Read camera until q key is pressed
while True:
    ret, frame = cam.read()

    BG = cv2.bitwise_and(frame,frame,mask=BGMask)
    
    cv2.imshow('BG',BG)
    cv2.moveWindow('BG', 703, 100)

    compImage = cv2.add(BG,FG)
    cv2.imshow('compImage', compImage)
    cv2.moveWindow('compImage', 1017, 100)

    blendValue = cv2.getTrackbarPos('blendValue', 'blended')/100
    blendValue2 = 1-blendValue

    blended = cv2.addWeighted(frame, blendValue, cvLogo, blendValue2, 0)
    cv2.imshow('blended', blended)
    cv2.moveWindow('blended', 1017, 350)

    FG2 = cv2.bitwise_and(blended, blended, mask = FGMask)
    cv2.imshow('FG2', FG2)
    cv2.moveWindow('FG2', 1324, 100)

    compFinal = cv2.add(BG,FG2)
    cv2.imshow('compFinal', compFinal)
    cv2.moveWindow('compFinal', 1324, 350)  

    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 100)
    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()