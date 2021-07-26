#program launches the rpi cam with jetson nano

import cv2

print(cv2.__version__)

#Setting up the camera
dispW=640
dispH=480
flip=0

def nothing(x):
    pass

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(camSet)
cv2.namedWindow('piCam')
cv2.createTrackbar('xVal', 'piCam', 25, dispW, nothing)
cv2.createTrackbar('yVal', 'piCam', 25, dispH, nothing)
cv2.createTrackbar('width', 'piCam', 25, dispW, nothing)
cv2.createTrackbar('height', 'piCam', 25, dispW, nothing)

#Read camera until q key is pressed
while True:
    ret, frame = cam.read()
    xVal = cv2.getTrackbarPos('xVal', 'piCam')
    yVal = cv2.getTrackbarPos('yVal', 'piCam')
    width = cv2.getTrackbarPos('width', 'piCam')
    height = cv2.getTrackbarPos('height', 'piCam')
    #cv2.circle(frame, (xVal, yVal), 5, (255,0,0), -1)
    cv2.rectangle(frame, (xVal,yVal), ((xVal+width),(yVal+height)), (255,0,0), 4)
    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 0)
    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()