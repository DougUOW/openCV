#program launches the logitech web cam with jetson nano

import cv2

print(cv2.__version__)

#Without the cam.set command, will use maximum HD resolution, which causes way to much lag in
#the system. Raw image is now grabbed at 640 x 480
cam = cv2.VideoCapture(1)
cam.set(3,640)
cam.set(4,480)

#Read camera until q key is pressed
while True:
    ret, frame = cam.read()
    cv2.imshow('piCam',frame)
    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()