""" Experiment with card detection and filtering using OpenCV """
''' SoftDes MP4: Interactive Programming - Isaac Vandor & Raquel Dunoff '''
''' Open camera and show detected card'''

# Import necessary packages
import cv2
import numpy as np
import time
import os
import card_setup

# Define constants and initialize variables

# Camera settings
IM_WIDTH = 1280
IM_HEIGHT = 720
FRAME_RATE = 10

## Define font to use
font = cv2.FONT_HERSHEY_DUPLEX

# Initialize camera object and video feed from the camera. Change integer to reflect internal webcam versus usb webcam.
video_stream = cv2.VideoCapture(1)
time.sleep(1) # Give the camera time to warm up

# Load the train rank and suit images
path = os.path.dirname(os.path.abspath(__file__))
train_ranks = card_setup.load_ranks( path + '/card_imgs/')
train_suits = card_setup.load_suits( path + '/card_imgs/')


'''
Grab frames from the video stream
and process them to find and identify playing cards.
'''

cam_quit = 0 # Loop control variable

# Begin capturing frames
while cam_quit == 0:

    # Grab frame from video stream
    #image = videostream.read()
    ret, image = video_stream.read()

    # Pre-process camera image (gray, blur, and threshold it)
    pre_proc = card_setup.preprocess_image(image)

    # Find and sort the contours of all cards in the image (query cards)
    contours_sort, contour_is_card = card_setup.find_cards(pre_proc)

    # If there are no contours, do nothing
    if len(contours_sort) != 0:

        # Initialize a new "cards" list to assign the card objects w/ k as index.
        cards = []
        k = 0

        # For each contour detected:
        for i in range(len(contours_sort)):
            if (contour_is_card[i] == 1):

                # Append card object and run preprocess_card func. to generate
                # flattened image and isolate card suit and rank
                cards.append(card_setup.preprocess_card(contours_sort[i],image))

                # Find the best rank and suit match for the card.
                cards[k].best_rank_match,cards[k].best_suit_match,cards[k].rank_diff,cards[k].suit_diff = card_setup.match_card(cards[k],train_ranks,train_suits)

                # Draw center point and match result on the image.
                image, rank_name, suit_name = card_setup.draw_results(image, cards[k])
                k = k + 1

        # Draw card contours on image
        if (len(cards) != 0):
            temp_contours = []
            for i in range(len(cards)):
                temp_contours.append(cards[i].contour)
            cv2.drawContours(image,temp_contours, -1, (0,0,0), 3)
            cv2.drawContours(image,temp_contours, -1, (255,150,20), 2)

    # Finally, display the image
    cv2.imshow("Playing Card Detector",image)

    # Poll the keyboard. If 'q' is pressed, exit the program.
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = 1


# Close all windows and close the video feed.
cv2.destroyAllWindows()
cap.release()
