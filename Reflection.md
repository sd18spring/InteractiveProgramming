# Mini-Project 4: Interactive Programming
### OpenCV Fruit Ninja
### By: Amy Phung and Sid Garimella

## Project Overview
We created a game similar to Fruit Ninja where players could use their hands as the controller. By waving their hands in front of a webcam, they could cut virtual fruits if their hands are positioned at the correct places.

## Results
Our final product was a successful proof of concept game where basic game functions and the game controller were implemented, but did not have a completed UI.
Hands move, fruits disappear, fruits were "tossed" onscreen, basic sound effects

(include game screenshots)

## Implementation
We used the model-view-controller construction to create this game

#### Model:
Objects: fruit, hand-coordinates set to output of controller coordinates

randomly create fruit objects with adjustable parameters, and if the coordinates of the hand is in the area of the fruit, then the fruit is destroyed

#### View:
Each fruit object was a colored circle centered around the current coordinates of the fruit. The hand was represented with a small white circle so players could know where their hands were in-game. 

#### Controller:
For each frame in a webcam feed, the image is blurred and a mask is applied to create a binary image in which only colors in a particular color range (for which we used skin colors) are white and the rest is black. The largest continuous area in the binary image is considered to be the hand, and the script computes the center of the hand based on this area. It passes the coordinates of the center to the model.

#### Integration:
The model, view, and controller aspects of our game all had to be repeatedly updated based on the camera input, so all three were integrated into the same while loop. During each loop, the game checked the webcamm feed to obtain coordinates of the hand, checked to see if there were any collisions between the hand coordinate and a fruit, then updated the game by deleting "sliced" fruits and moving the intact ones. 


## Reflection
