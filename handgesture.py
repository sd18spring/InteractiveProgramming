

import numpy as np
import cv2


cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert to HVS
    hsv_scale = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)

    # defining range of blue
    lower_threshold = np.array([110,50,50])
    upper_threshold = np.array([130,255,255])


    # creating the threshold

    # binary
    mask = cv2.inRange(hsv_scale, lower_threshold, upper_threshold)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # blue
    res = cv2.bitwise_and(frame,frame,mask=mask)


    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    im2, contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(imgray, contours, 0, (0,255,0), 3)



    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('gray', imgray)
    cv2.imshow('res', res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
