""" Experiment with card detection and filtering using OpenCV """
''' SoftDes MP4: Interactive Programming - Isaac Vandor & Raquel Dunoff '''
''' Card rank/suit training and classification'''


# Import necessary packages
import numpy as np
import cv2
import time

'''
Variables for dimensions, thresholding, and calculating difference between
unknown and training cards
'''

# Light threshold levels
background_threshold = 60
card_threshold = 30

# Width and height of card corner
corner_width = 32
corner_height = 84

# Dimensions of rank training images
rank_width = 70
rank_height = 125

# Dimensions of suit training images
suit_width = 70
suit_height = 100

# Maximum differences between cards for rank & suit
max_rank_difference = 2000
max_suit_difference = 700

# Maximum/Minimum card area dimensions
max_card_area = 120000
min_card_area = 25000

# Fonts....cuz apparently opencv loves the Hershey font
font = cv2.FONT_HERSHEY_DUPLEX

'''
Create clases to store unknown card information and training data
'''

class Unknown_card:
    '''Structure to store information about unknown cards in the image frame.'''

    def __init__(self):
        self.contour = [] # Contour of card
        self.width, self.height = 0, 0 # Width and height of card
        self.corner_pts = [] # Corner points of card
        self.center = [] # Center point of card
        self.warp = [] # 200x300, flattened, grayed, blurred image
        self.rank_img = [] # Thresholded, sized image of card's rank
        self.suit_img = [] # Thresholded, sized image of card's suit
        self.best_rank_match = "Unknown" # Best matched rank
        self.best_suit_match = "Unknown" # Best matched suit
        self.rank_difference = 0 # Difference between rank image and best matched train rank image
        self.suit_difference = 0 # Difference between suit image and best matched train suit image

class Rank_training:
    """Structure to store information about card rank images."""

    def __init__(self):
        self.img = [] # Thresholded, sized rank image
        self.name = "Placeholder"

class Suit_training:
    """Structure to store information about card suit images."""

    def __init__(self):
        self.img = [] # Thresholded, sized suit image
        self.name = "Placeholder"

'''Functions to handle rank and suit sorting'''

def load_ranks(filepath):
    '''Load rank images from directory and store
    them in a list of rank_training objects.'''

    rank_training = []
    i = 0

    for Rank in ['Ace','Two','Three','Four','Five','Six','Seven',
                 'Eight','Nine','Ten','Jack','Queen','King']:
        rank_training.append(Rank_training())
        rank_training[i].name = Rank
        filename = Rank + '.jpg'
        rank_training[i].img = cv2.imread(filepath+filename, cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return rank_training

def load_suits(filepath):
    '''Load suit images from directory and store
    them in a list of suit_training objects.'''

    suit_training = []
    i = 0

    for Suit in ['Spades','Diamonds','Clubs','Hearts']:
        suit_training.append(Suit_training())
        suit_training[i].name = Suit
        filename = Suit + '.jpg'
        suit_training[i].img = cv2.imread(filepath+filename, cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return suit_training

def preprocess_image(image):
    '''Returns a grayed, blurred, and thresholded camera image.'''

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    '''
    Tries to adaptively change threshold based on lighting conditions
    A background pixel in the center top of the image is sampled to determine
    its intensity.
    '''
    img_width, img_height = np.shape(image)[:2]
    background_level = gray[int(img_height/100)][int(img_width/2)]
    threshold_level = background_threshold + background_level

    retval, threshold = cv2.threshold(blur,threshold_level,255,cv2.THRESH_BINARY)

    return threshold

def find_cards(threshold_image):
    '''Finds all card-sized contours in a thresholded camera image.
    Returns the number of cards and a list of card contours sorted
    from largest to smallest.'''

    # Find contours and sort their indices by contour size
    dummy,contours,hierarchy = cv2.findContours(threshold_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    index_sort = sorted(range(len(contours)), key=lambda i : cv2.contourArea(contours[i]),reverse=True)

    # If there are no contours, do nothing
    if len(contours) == 0:
        return [], []

    # Otherwise, initialize empty sorted contour and hierarchy lists
    contours_sort = []
    hierarchy_sort = []
    contour_is_card = np.zeros(len(contours),dtype=int)

    # Fill empty lists with sorted contour and sorted hierarchy. Now,
    # the indices of the contour list still correspond with those of
    # the hierarchy list. The hierarchy array can be used to check if
    # the contours have parents or not.
    for i in index_sort:
        contours_sort.append(contours[i])
        hierarchy_sort.append(hierarchy[0][i])

    '''
    Determine which of the contours are cards by applying the
    following criteria:
    1) smaller area than the maximum card size
    2) bigger area than the minimum card size
    3) have no parents
    4) have four corners
    '''
    for i in range(len(contours_sort)):
        size = cv2.contourArea(contours_sort[i])
        perimeter = cv2.arcLength(contours_sort[i],True)
        approx = cv2.approxPolyDP(contours_sort[i],0.01*perimeter,True)

        if ((size < max_card_area) and (size > min_card_area)
            and (hierarchy_sort[i][3] == -1) and (len(approx) == 4)):
            contour_is_card[i] = 1

    return contours_sort, contour_is_card

def preprocess_card(contour, image):
    '''Uses contour to find information about the unknown card. Isolates rank
    and suit images from the card.'''

    # Initialize new Unknown_card object
    unknownCard = Unknown_card()

    unknownCard.contour = contour

    # Find perimeter of card and use it to approximate corner points
    perimeter = cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour,0.01*perimeter,True)
    pts = np.float32(approx)
    unknownCard.corner_pts = pts

    # Find width and height of card's bounding rectangle
    x,y,width,height = cv2.boundingRect(contour)
    unknownCard.width, unknownCard.height = width, height

    # Find center point of card by taking x and y average of the four corners.
    average = np.sum(pts, axis=0)/len(pts)
    cent_x = int(average[0][0])
    cent_y = int(average[0][1])
    unknownCard.center = [cent_x, cent_y]

    # Warp card into 200x300 flattened image using perspective transform
    unknownCard.warp = flattener(image, pts, width, height)

    # Grab corner of warped card image and do a 4x zoom
    unknown_corner = unknownCard.warp[0:corner_height, 0:corner_width]
    unknown_corner_zoom = cv2.resize(unknown_corner, (0,0), fx=4, fy=4)

    # Sample known white pixel intensity to determine good threshold level
    white_level = unknown_corner_zoom[15,int((corner_width*4)/2)]
    threshold_level = white_level - card_threshold
    if (threshold_level <= 0):
        threshold_level = 1
    retval, unknown_threshold = cv2.threshold(unknown_corner_zoom, threshold_level, 255, cv2. THRESH_BINARY_INV)

    # Split in to top and bottom half (top shows rank, bottom shows suit)
    unknown_rank = unknown_threshold[20:185, 0:128]
    unknown_suit = unknown_threshold[186:336, 0:128]

    # Find rank contour and bounding rectangle, isolate and find largest contour
    dummy, unknown_rank_contours, hierarchy = cv2.findContours(unknown_rank, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    unknown_rank_contours = sorted(unknown_rank_contours, key=cv2.contourArea,reverse=True)

    # Find bounding rectangle for largest contour, use it to resize unknown rank
    # image to match dimensions of the rank_training image
    if len(unknown_rank_contours) != 0:
        x1,y1,w1,h1 = cv2.boundingRect(unknown_rank_contours[0])
        unknown_rank_roi = unknown_rank[y1:y1+h1, x1:x1+w1]
        unknown_rank_sized = cv2.resize(unknown_rank_roi, (rank_width,rank_height), 0, 0)
        unknownCard.rank_img = unknown_rank_sized

    # Find suit contour and bounding rectangle, isolate and find largest contour
    dummy, unknown_suit_contours, hierarchy = cv2.findContours(unknown_suit, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    unknown_suit_contours = sorted(unknown_suit_contours, key=cv2.contourArea,reverse=True)

    # Find bounding rectangle for largest contour, use it to resize unknown suit
    # image to match dimensions of the suit_training image
    if len(unknown_suit_contours) != 0:
        x2,y2,w2,h2 = cv2.boundingRect(unknown_suit_contours[0])
        unknown_suit_roi = unknown_suit[y2:y2+h2, x2:x2+w2]
        unknown_suit_sized = cv2.resize(unknown_suit_roi, (suit_width, suit_height), 0, 0)
        unknownCard.suit_img = unknown_suit_sized

    return unknownCard

def match_card(unknownCard, rank_training, suit_training):
    '''Finds best rank and suit matches for the unknown card. Differences
    the unknown card rank and suit images with the train rank and suit images.
    The best match is the rank or suit image that has the least difference.'''

    best_rank_match_difference = 10000
    best_suit_match_difference = 10000
    best_rank_match_name = "Unknown"
    best_suit_match_name = "Unknown"
    i = 0

    '''
    If no contours were found in unknown card in preprocess_card function,
    the img size is zero, so skip the difference process and leave card as unknown
    '''
    if (len(unknownCard.rank_img) != 0) and (len(unknownCard.suit_img) != 0):
        '''
        Find the difference the unknown card rank image from each of the train rank images,
        and store the result with the least difference
        '''
        for unknown_rank in rank_training:

                image_difference = cv2.absdiff(unknownCard.rank_img, unknown_rank.img)
                rank_difference = int(np.sum(image_difference)/255)

                if rank_difference < best_rank_match_difference:
                    best_rank_difference_img = image_difference
                    best_rank_match_difference = rank_difference
                    best_rank_name = unknown_rank.name

        # Find the difference for suit images and store result
        for unknown_suit in suit_training:

                image_difference = cv2.absdiff(unknownCard.suit_img, unknown_suit.img)
                suit_difference = int(np.sum(image_difference)/255)

                if suit_difference < best_suit_match_difference:
                    best_suit_difference_img = image_difference
                    best_suit_match_difference = suit_difference
                    best_suit_name = unknown_suit.name

    '''
    Combine best rank and best suit match to get unknown card's identity.
    If the best matches have too high of a difference value, card identity
    is still unknown
    '''
    if (best_rank_match_difference < max_rank_difference):
        best_rank_match_name = best_rank_name

    if (best_suit_match_difference < max_suit_difference):
        best_suit_match_name = best_suit_name

    # Return the identiy of the card and the quality of the suit and rank match
    return best_rank_match_name, best_suit_match_name, best_rank_match_difference, best_suit_match_difference


def draw_results(image, unknownCard):
    '''Draw the card name, center point, and contour on the image frame.'''
    #card_results = []

    x = unknownCard.center[0]
    y = unknownCard.center[1]
    cv2.circle(image,(x,y),5,(255,0,0),-1)

    rank_name = unknownCard.best_rank_match
    suit_name = unknownCard.best_suit_match

    #card_results = [rank_name, suit_name]
    #print(card_results)

    # Draw card name twice, so letters have black outline
    cv2.putText(image,(rank_name+' of'),(x-60,y-10),font,1,(0,0,0),3,cv2.LINE_AA)
    cv2.putText(image,(rank_name+' of'),(x-60,y-10),font,1,(200,200,200),2,cv2.LINE_AA)

    cv2.putText(image,suit_name,(x-60,y+25),font,1,(0,0,0),3,cv2.LINE_AA)
    cv2.putText(image,suit_name,(x-60,y+25),font,1,(200,200,200),2,cv2.LINE_AA)
    #print(rank_name+' of', suit_name)
    '''
    Can draw difference value for troubleshooting purposes
    rank_difference = str(unknownCard.rank_difference)
    suit_difference = str(unknownCard.suit_difference)
    cv2.putText(image,rank_difference,(x+20,y+30),font,0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(image,suit_difference,(x+20,y+50),font,0.5,(0,0,255),1,cv2.LINE_AA)
     '''
    return image, rank_name, suit_name

def flattener(image, pts, w, h):
    '''
    Flattens an image of a card into a top-down 200x300 perspective.
    Returns the flattened, re-sized, grayed image.
    See www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
    '''
    temp_rect = np.zeros((4,2), dtype = "float32")

    s = np.sum(pts, axis = 2)

    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]

    diff = np.diff(pts, axis = -1)
    tr = pts[np.argmin(diff)]
    bl = pts[np.argmax(diff)]

    # Need to create an array listing points in order of
    # [top left, top right, bottom right, bottom left]
    # before doing the perspective transform

    if w <= 0.8*h: # If card is vertically oriented
        temp_rect[0] = tl
        temp_rect[1] = tr
        temp_rect[2] = br
        temp_rect[3] = bl

    if w >= 1.2*h: # If card is horizontally oriented
        temp_rect[0] = bl
        temp_rect[1] = tl
        temp_rect[2] = tr
        temp_rect[3] = br

    # If the card is 'diamond' oriented, a different algorithm
    # has to be used to identify which point is top left, top right
    # bottom left, and bottom right.

    if w > 0.8*h and w < 1.2*h: #If card is diamond oriented
        # If furthest left point is higher than furthest right point,
        # card is tilted to the left.
        if pts[1][0][1] <= pts[3][0][1]:
            # If card is titled to the left, approxPolyDP returns points
            # in this order: top right, top left, bottom left, bottom right
            temp_rect[0] = pts[1][0] # Top left
            temp_rect[1] = pts[0][0] # Top right
            temp_rect[2] = pts[3][0] # Bottom right
            temp_rect[3] = pts[2][0] # Bottom left

        # If furthest left point is lower than furthest right point,
        # card is tilted to the right
        if pts[1][0][1] > pts[3][0][1]:
            # If card is titled to the right, approxPolyDP returns points
            # in this order: top left, bottom left, bottom right, top right
            temp_rect[0] = pts[0][0] # Top left
            temp_rect[1] = pts[3][0] # Top right
            temp_rect[2] = pts[2][0] # Bottom right
            temp_rect[3] = pts[1][0] # Bottom left


    max_width = 200
    max_height = 300

    # Create destination array, calculate perspective transform matrix,
    # and warp card image
    dst = np.array([[0,0],[max_width-1,0],[max_width-1,max_height-1],[0, max_height-1]], np.float32)
    M = cv2.getPerspectiveTransform(temp_rect,dst)
    warp = cv2.warpPerspective(image, M, (max_width, max_height))
    warp = cv2.cvtColor(warp,cv2.COLOR_BGR2GRAY)

    return warp
