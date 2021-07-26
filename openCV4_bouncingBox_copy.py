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
ballHeightTop = 20
ballHeightBottom = 460
ballWidthLeft = 20
ballWidthRight = 620
i = 0
flagHeight = 0
flagWidth = 0

while True:
    ret, frame = cam.read()
    frame = cv2.circle(frame, (ballWidthLeft,ballHeightBottom), 20, (0,255,0), -1)
    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 0)
    
    if flagHeight == 0:
        ballHeightBottom = ballHeightBottom + 1
        if ballHeightBottom == 461:
            ballHeightBottom = ballHeightBottom - 2
            flagHeight = 1
    if flagHeight == 1:
        ballHeightBottom = ballHeightBottom - 1
        if ballHeightBottom == 19:
            ballHeightBottom = ballHeightBottom + 2
            flagHeight = 0  

    if flagWidth == 0:
        ballWidthLeft = ballWidthLeft + 1
        if ballWidthLeft == 621:
            ballWidthLeft = ballWidthLeft - 2
            flagWidth = 1
    if flagWidth == 1:
        ballWidthLeft = ballWidthLeft - 1
        if ballWidthLeft == 19:
            ballWidthLeft = ballWidthLeft + 2
            flagWidth = 0       

    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()