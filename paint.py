
import cv2
import numpy as np

"""capturing video from camera"""
cap = cv2.VideoCapture(0)
frame_num = 0
cx = 0
cy = 0
path = []

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


    mask1 = cv2.inRange(hsv, np.array([0, 150, 100]), np.array([5, 255, 255]));
    mask2 = cv2.inRange(hsv, np.array([175, 150, 100]), np.array([180, 255, 255]));
    mask = mask1 | mask2
    mask = cv2.bilateralFilter(mask, 10, 40, 40)
    mask = cv2.blur(mask,(5,5))

    res = cv2.bitwise_and(frame,frame,mask=mask)
    mask = cv2.blur(mask,(20,20))
    # Getting a contour and the center of the contour
    im2,contours,hierarchy = cv2.findContours(mask, 1, 2)
    try:
        if frame_num > 3 or frame_num == 0:
            cnt = contours[0]
            M = cv2.moments(cnt)
            print(M['m10']/M['m00'])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            frame_num = 0
            path.append((cx, cy))
        cv2.circle(res, (cx, cy), 2, (0, 255, 0), -1)
    except IndexError:
        """"""

    for i in range(len())
    frame_num += 1
    # cnts = cv2.findContours(res, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #display the resulting frame
    cv2.imshow('frame',frame)
    #cv2.imshow('mask', mask)
    cv2.imshow('res',res)
    # cv2.imshow('counto', )
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
