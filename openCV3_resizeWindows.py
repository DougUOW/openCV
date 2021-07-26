#program launches the rpi cam with jetson nano
#demonstrating how to move and resize video streams
import cv2

print(cv2.__version__)

#Setting up the camera
dispW=640
dispH=480
flip=0
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(camSet)

#Read camera until q key is pressed
while True:
    ret, frame = cam.read()
    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 0)
    #create gray version of original image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #create small versions of frame and gray
    frameSmall = cv2.resize(frame, (320, 240))
    graySmall = cv2.resize(gray, (320, 240))
    
    cv2.imshow('Frame Small', frameSmall)
    cv2.imshow('Gray Small', graySmall)

    cv2.moveWindow('Frame Small', 0, 530)
    cv2.moveWindow('Gray Small', 380, 530)
   
    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()