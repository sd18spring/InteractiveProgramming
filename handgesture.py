import numpy as np
from collections import deque
import cv2


cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert to HSV
    hsv_scale = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)


    # defining range of blue
    lower_threshold_blue = np.array([110,50,50])
    upper_threshold_blue = np.array([130,255,255])

    # creating the threshold
    # binary
    mask = cv2.inRange(hsv_scale, lower_threshold_blue, upper_threshold_blue)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)


    # blue moment tracking
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    blue_coordinates = []

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)


    # definng range of red
    lower_threshold_red = np.array([0,100,100])
    upper_threshold_red = np.array([179,255,255])

    mask2 = cv2.inRange(hsv_scale, lower_threshold_red, upper_threshold_red)
    mask2 = cv2.erode(mask2, None, iterations=2)
    mask2 = cv2.dilate(mask2, None, iterations=2)

    # blue moment tracking
    contours2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center2 = None

    if len(contours2) > 0:

        c = max(contours2, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center2 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
        cv2.circle(frame, center2, 5, (0, 0, 255), -1)


    # blue
    res = cv2.bitwise_and(frame,frame,mask=mask)


    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('mask2', mask2)
    cv2.imshow('res', res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
