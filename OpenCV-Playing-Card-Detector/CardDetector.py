############## Python-OpenCV Playing Card Detector ###############
#
# Author: Evan Juras
# Date: 9/5/17
# Description: Python script to detect and identify playing cards
# from a PiCamera video feed.
#

# Import necessary packages
import cv2
import numpy as np
import time
import os
import Cards
import VideoStream


### ---- INITIALIZATION ---- ###
# Define constants and initialize variables

## Camera settings
IM_WIDTH = 1280
IM_HEIGHT = 720 
FRAME_RATE = 10

## Initialize calculated frame rate because it's calculated AFTER the first time it's displayed
frame_rate_calc = 1
freq = cv2.getTickFrequency()

## Define font to use
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize camera object and video feed from the camera. The video stream is set up
# as a seperate thread that constantly grabs frames from the camera feed. 
# See VideoStream.py for VideoStream class definition
## IF USING USB CAMERA INSTEAD OF PICAMERA,
## CHANGE THE THIRD ARGUMENT FROM 1 TO 2 IN THE FOLLOWING LINE:
videostream = VideoStream.VideoStream((IM_WIDTH,IM_HEIGHT),FRAME_RATE,1,0).start()
time.sleep(1) # Give the camera time to warm up

# Load the train rank and suit images
path = os.path.dirname(os.path.abspath(__file__))
train_ranks = Cards.load_ranks( path + '/New_Cards/')
train_suits = Cards.load_suits( path + '/New_Cards/')


### ---- MAIN LOOP ---- ###
# The main loop repeatedly grabs frames from the video stream
# and processes them to find and identify playing cards.

cam_quit = 0 # Loop control variable
print("Begin main loop")
# Begin capturing frames
while cam_quit == 0:

    # Grab frame from video stream
    image = videostream.read()
    
    image =cv2.flip(image, -1)
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()

    # Pre-process camera image (gray, blur, and threshold it)
    pre_proc = Cards.preprocess_image(image)
	
    # Find and sort the contours of all cards in the image (query cards)
    cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)
    cards = []
    # If there are no contours, do nothing
    if len(cnts_sort) != 0:

        # Initialize a new "cards" list to assign the card objects.
        # k indexes the newly made array of cards.
        cards = []
        k = 0

        # For each contour detected:
        for i in range(len(cnts_sort)):
            if (cnt_is_card[i] == 1):

                # Create a card object from the contour and append it to the list of cards.
                # preprocess_card function takes the card contour and contour and
                # determines the cards properties (corner points, etc). It generates a
                # flattened 200x300 image of the card, and isolates the card's
                # suit and rank from the image.
                cards.append(Cards.preprocess_card(cnts_sort[i],image))

                # Find the best rank and suit match for the card.
                cards[k].best_rank_match,cards[k].best_suit_match,cards[k].rank_diff,cards[k].suit_diff = Cards.match_card(cards[k],train_ranks,train_suits)

                # Draw center point and match result on the image.
                image = Cards.draw_results(image, cards[k])
                k = k + 1
	    
        # Draw card contours on image (have to do contours all at once or
        # they do not show up properly for some reason)
        if (len(cards) != 0):
            temp_cnts = []
            for i in range(len(cards)):
                temp_cnts.append(cards[i].contour)
            cv2.drawContours(image,temp_cnts, -1, (255,0,0), 2)
    dealer_cards = []
    player_cards = []
    #find dealer cards
    for i in range(len(cards)):
        print(cards[i].center)
        if (cards[i].center[1]>300):
            player_cards.append(cards[i])
        else:
            dealer_cards.append(cards[i])
    
    # Draw framerate in the corner of the image. Framerate is calculated at the end of the main loop,
    # so the first time this runs, framerate will be shown as 0.
    cv2.putText(image,"FPS: "+str(int(frame_rate_calc)),(10,26),font,0.7,(255,0,255),2,cv2.LINE_AA)
    
    
    #calc current number
    player_sum = 0
    dealer_sum = 0
    for i in range(len(dealer_cards)):
        if(dealer_cards[i].best_rank_match == "Unknown"):
            dealer_sum += 0
        elif(dealer_cards[i].best_rank_match == "Six"):
            dealer_sum += 6 
        elif(dealer_cards[i].best_rank_match == "Nine"):
            dealer_sum += 9 
        else:
            dealer_sum += int(dealer_cards[i].best_rank_match)
    

    for i in range(len(player_cards)):
        if(player_cards[i].best_rank_match == "Unknown"):
            player_sum += 0
        elif(player_cards[i].best_rank_match == "Six"):
            player_sum += 6 
        elif(player_cards[i].best_rank_match == "Nine"):
            player_sum += 9 
        else:
            player_sum += int(player_cards[i].best_rank_match)
    
    cv2.putText(image,"# player cards: "+str(len(player_cards))+" with "+str(player_sum) ,(10,80),font,0.7,(255,0,255),2,cv2.LINE_AA)

    cv2.putText(image,"# dealer cards: "+str(len(dealer_cards)) + " with "+str(dealer_sum),(10,50),font,0.7,(255,0,255),2,cv2.LINE_AA)
    
    recommend = "?"
    proba = 0.0
    # Should implement by DH


    action = "BEST ACTION: " + recommend + " with probability " + str(proba)
    
    cv2.putText(image,action,(10,110),font,0.7,(255,0,255),2,cv2.LINE_AA)
    

    cv2.line(image, (0, 320), (1280, 320), (0,255,0), 2)
    # Finally, display the image with the identified cards!
    cv2.imshow("Card Detector",image)

    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc = 1/time1
    
    # Poll the keyboard. If 'q' is pressed, exit the main loop.
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = 1
        

# Close all windows and close the PiCamera video stream.
cv2.destroyAllWindows()
videostream.stop()

