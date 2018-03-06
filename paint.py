
import cv2
import numpy as np

"""capturing video from camera"""
cap = cv2.VideoCapture(0)

while(True):
    #capture frame by frame
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #find specific color
    lower_white = np.array([[0, 0, 230]])
    upper_white = np.array([180, 25, 255])
    lower_color = np.array([0,80,50])
    upper_color = np.array([20,100,100])
    lower_red = np.array([150,150,50])
    upper_red = np.array([180,255,150])

    mask = cv2.inRange(hsv,lower_red, upper_red)

    res = cv2.bitwise_and(frame,frame,mask=mask)

    #display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res',res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#when finshed, release the capture
cap.release()
cv2.destroyAllWindows()
"""playing video from file
cap = cv2.VideoCapture('test.avi')

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.waitKey(25)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
"""
