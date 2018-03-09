import cv2
import numpy as np


input_cam = 0

minLength = 15
minPassLength = 50
maxGap = 6

canny_arpeture = 3
canny_threshold = 99
filter_threshold = 378

c_alpha = 2
c_beta = 50

cam = cv2.VideoCapture(input_cam)

while(True):

	#-- RETRIEVE FRAME FROM VIDEO AS IMAGE

	ret, frame = cam.read()

	#-- IMAGE PREPROCESSING -- GRAYSCALE, BILAT FILTER, CANNY EDGE DETECTION

	blackout = np.zeros((480,650,3),np.uint8) 
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	#frame.convertTo(gray_contrast, -1, c_alpha, c_beta);

	filtered_gray = cv2.bilateralFilter(gray,9,100,filter_threshold)


	edges = cv2.Canny(filtered_gray, 0, canny_threshold,apertureSize=canny_arpeture) 

	#-- PROBABLISTIC HOUGH TRANSFORMATION 1-- 

	lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLength, maxGap)

	try:
		for x1,y1,x2,y2 in lines[0]:
			cv2.line(blackout,(x1,y1),(x2,y2),(0,255,0),3)
	except TypeError:
		pass

	#-- HOUGH TRANSFORMATION -- VANISHING POINT LINES

	gray_v = cv2.cvtColor(blackout,cv2.COLOR_BGR2GRAY)
	lines_v = cv2.HoughLines(gray_v, 1, np.pi/180, 150)
	

	try:
		for rho,theta in lines_v[0]:

		    a = np.cos(theta)
		    b = np.sin(theta)
		    x0 = a*rho
		    y0 = b*rho
		    x1 = int(x0 + 1000*(-b))
		    y1 = int(y0 + 1000*(a))
		    x2 = int(x0 - 1000*(-b))
		    y2 = int(y0 - 1000*(a))
		    cv2.line(blackout,(x1,y1),(x2,y2),(0,0,255),2)

	except TypeError:
		pass


	#-- DISPLAYING OUTPUT --

	cv2.imshow('LINES',blackout)
	cv2.imshow('GRAYSCALE',gray)
	cv2.imshow('GRAYSCALE_FILTERED',filtered_gray)
	cv2.imshow('CANNY EDGE', edges)
	#cv2.imshow('CONTRAST', gray_contrast)

	if cv2.waitKey(10) & 0xff == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()

#NOTES: add contrast, try kap filter