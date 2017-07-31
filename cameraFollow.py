import numpy as np
import cv2
import time
import os
import imutils
from imutils.video.pivideostream import PiVideoStream


# This system command loads the right drivers for the Raspberry Pi camera
#os.system('sudo modprobe bcm2835-v4l2')

w=240
h=180

my_camera = PiVideoStream().start()

time.sleep(2)

while (True):
    image = my_camera.read()
    image = cv2.flip(image,-1)
    image = imutils.resize(image, width=240, height=180)
    image = cv2.GaussianBlur(image,(5,5),0)

    image_HSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_pink = np.array([6,200,66])
    upper_pink = np.array([15,255,133])
    mask = cv2.inRange(image_HSV,lower_pink,upper_pink)
    mask = cv2.GaussianBlur(mask,(5,5),0)

    # findContours returns a list of the outlines of the white shapes in the mask (and a heirarchy that we shall ignore)
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # If we have at least one contour, look through each one and pick the biggest
    if len(contours)>0:
        largest = 0
        area = 0
        for i in range(len(contours)):
            # get the area of the ith contour
            temp_area = cv2.contourArea(contours[i])
            # if it is the biggest we have seen, keep it
            if temp_area > area:
                area = temp_area
                largest = i
        # Compute the coordinates of the center of the largest contour
        coordinates = cv2.moments(contours[largest])
        target_x = int(coordinates['m10']/coordinates['m00'])
        target_y = int(coordinates['m01']/coordinates['m00'])
        # Pick a suitable diameter for our target (grows with the contour)
        diam = int(np.sqrt(area)/4)
        print("X " +str(target_x) + " Y " + str(target_y) + " A " + str(diam))
        # draw on a target
        cv2.circle(image,(target_x,target_y),diam,(0,255,0),1)
        cv2.line(image,(target_x-2*diam,target_y),(target_x+2*diam,target_y),(0,255,0),1)
        cv2.line(image,(target_x,target_y-2*diam),(target_x,target_y+2*diam),(0,255,0),1)
    cv2.imshow('View',image)
 # Esc key to stop, otherwise repeat after 3 milliseconds
    if cv2.waitKey(1) & 0xFF == 27:
        my_camera.release()

cv2.destroyAllWindows()
my_camera.release()
# due to a bug in openCV you need to call wantKey three times to get the
# window to dissappear properly. Each wait only last 10 milliseconds
cv2.waitKey(10)
time.sleep(0.1)
cv2.waitKey(10)
cv2.waitKey(10)