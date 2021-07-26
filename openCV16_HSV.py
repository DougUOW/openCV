#Program will read a pic (smarties.png) from file, then by converting the image into the
#HSV color space, identify the various colors in the image. Trackbars are used to make
#colour selection easier.

#As in the HSV colour space, red goes from roughly 160 - 20, we ned to use 2 trackbars and
#seperate arrays, as we need to get the values 160-179 and 0 to 20, then combine them into one array.

import cv2
import numpy as np  #numpy is the mathematical library that works with arrays.

#Dummy function as createTrackbar function requires it.
def nothing(x):
    pass

#Setup trackbars that allow us to quickly change HSV values
cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars', 1320, 0)
cv2.createTrackbar('hueLow', 'Trackbars', 50, 179, nothing)
cv2.createTrackbar('hueHigh', 'Trackbars', 100, 179, nothing)

cv2.createTrackbar('hueLow2', 'Trackbars', 50, 179, nothing)
cv2.createTrackbar('hueHigh2', 'Trackbars', 100, 179, nothing)

cv2.createTrackbar('satLow', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('satHigh', 'Trackbars', 255, 255, nothing)

cv2.createTrackbar('valueLow', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('valueHigh', 'Trackbars', 255, 255, nothing)

while True:
    frame = cv2.imread('smarties.png')
    cv2.imshow('smarties',frame)
    cv2.moveWindow('smarties', 0, 0)

    #convert original image (frame) from BGR 2 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #Show HSV Image
    cv2.imshow('hsv', hsv)
    cv2.moveWindow('hsv', 480, 0)

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
    
    #Create foreground mask. Fuction only returns 1's and 0's. 1 for any pixel that
    #is in range, 0 for any vale out of range
    FGmask = cv2.inRange(hsv, lower_bound, upper_bound)
    FGmask2 = cv2.inRange(hsv, lower_bound2, upper_bound2)
    FGmaskcomp = cv2.add(FGmask,FGmask2)
    #Show the FGmask result
    cv2.imshow('FGmaskcomp', FGmaskcomp)
    cv2.moveWindow('FGmaskcomp', 0, 410)
    #Now AND the FGmask and the original image
    FG = cv2.bitwise_and(frame, frame, mask = FGmaskcomp)
    cv2.imshow('FG', FG)
    cv2.moveWindow('FG', 480, 410)

    #Create Background Mask. Just invert the FGmask
    BGmask = cv2.bitwise_not(FGmaskcomp)
    #Show the BGmask result
    cv2.imshow('BGmask', BGmask)
    cv2.moveWindow('BGmask', 900, 0)
    #Convert from grayscale to color matrix type
    BG = cv2.cvtColor(BGmask, cv2.COLOR_GRAY2BGR)
    cv2.imshow('BG', BG)
    cv2.moveWindow('BG', 900, 410)

    #Final Image. Add the Background and the Foreground
    final = cv2.add(FG,BG)
    cv2.imshow('final', final)
    cv2.moveWindow('final', 1320, 610)

    if cv2.waitKey(1) == ord('q'):
        break

#After q is pressed, release the camera back to the system
cam.release()
cv2.destroyAllWindows()