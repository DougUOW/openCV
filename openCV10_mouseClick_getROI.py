#program launches the rpi cam with jetson nano.
#program will identfy location of mouse button clicks

import cv2

print(cv2.__version__)

goFlag = 0

def click(event, x, y, flags, params):
    global x1,y1,x2,y2
    global goFlag
    if event == cv2.EVENT_LBUTTONDOWN:
        x1 = x
        y1 = y
        goFlag = 0
    if event == cv2.EVENT_LBUTTONUP:
        x2 = x
        y2 = y
        goFlag = 1

#Setting up the camera
dispW=640
dispH=480
flip=0

cv2.namedWindow('piCam')
cv2.setMouseCallback('piCam', click)

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)

#Read camera until q key is pressed
while True:
    ret, frame = cam.read()

    if goFlag == 1:
        frame = cv2.rectangle(frame, (x1,y1), (x2,y2), (255,0,0), 4)
        roi = frame[y1:y2, x1:x2]
        cv2.imshow('roi', roi)
        cv2.moveWindow('roi', 750, 0)

    cv2.imshow('piCam',frame)
    cv2.moveWindow('piCam', 0, 0)

    keyEvent = cv2.waitKey(1)
    if keyEvent == ord('c'):
        coord = []
    if keyEvent == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()