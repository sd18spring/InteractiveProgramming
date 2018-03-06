""" Experiment with card detection and filtering using OpenCV """
''' SoftDes MP4: Interactive Programming - Isaac Vandor & Raquel Dunoff '''
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(True):
    #Capture frame by frame
    ret, frame = cap.read()

    #Use the Haar Cascade face classifier
    #Change path to file path of .xml file on local machine after cloning
    face_cascade = cv2.CascadeClassifier('/home/isaac/InteractiveProgramming/haarcascade_frontalface_alt.xml')
    kernel = np.ones((21, 21), 'uint8')
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20, 20))

    #Loop for blurring and drawing all over faces
    for (x, y, w, h) in faces:
        '''
        center = (int(x+w/6),int(y+h/5))
        center2 = (int(x+(w*4)/6), int(y+h/5))
        center3 = (int(x+(w*3)/6), int(y+h/1.5))
        radius = (int(w/10))
        radius2 = (int(w/10))
        frame[y:y+h, x:x+w, :] = cv2.dilate(frame[y:y+h, x:x+w, :], kernel)
        cv2.ellipse(frame, center3,(100,50),0,0,180,255,-1)
        cv2.circle(frame, center, radius, (255,255,255), thickness=-1)
        cv2.circle(frame, center2, radius2, (255,255,255), thickness=-1)
        '''
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture when everything is done
cap.release()
cv2.destroyAllWindows()
