import cv2
import numpy as np                           #importing libraries

cap = cv2.VideoCapture(0)                #creating camera object
while( cap.isOpened() ) :
   ret,img = cap.read()                         #reading the frames
   cv2.imshow('input',img)                  #displaying the frames
   k = cv2.waitKey(10)
   if k == 27:
       break

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

max_area = 0
contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(contours)):
    cnt=contours[i]
    area = cv2.contourArea(cnt)
    if(area>max_area):
        max_area=area
        ci=i
    cnt=contours[ci]

hull = cv2.convexHull(cnt)

drawing = np.zeros(img.shape,np.uint8)
cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
cv2.drawContours(drawing,[hull],0,(0,0,255),2)

hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)

# def draw_hand_rect(self, frame):
#     rows,cols,_ = frame.shape
#
#     self.hand_row_nw = np.array([6*rows/20,6*rows/20,6*rows/20,10*rows/20,10*rows/20,10*rows/20,14*rows/20,14*rows/20,14*rows/20])
#
#     self.hand_col_nw = np.array([9*cols/20,10*cols/20,11*cols/20,9*cols/20,10*cols/20,11*cols/20,9*cols/20,10*cols/20,11*cols/20])
#
#     self.hand_row_se = self.hand_row_nw + 10
#     self.hand_col_se = self.hand_col_nw + 10
#
#     size = self.hand_row_nw.size
#     for i in range(size):
#         cv2.rectangle(frame,(self.hand_col_nw[i],self.hand_row_nw[i]),(self.hand_col_se[i],self.hand_row_se[i]),(0,255,0),1)
#         black = np.zeros(frame.shape, dtype=frame.dtype)
#         frame_final = np.vstack([black, frame])
#         return frame_final
