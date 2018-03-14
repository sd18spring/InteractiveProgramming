# Mini-Project 4: Interactive Programming
### OpenCV Fruit Ninja
### By: Amy Phung and Sid Garimella

## Project Overview
We created a game similar to Fruit Ninja where players could use their hands as the controller. By waving their hands in front of a webcam, they could cut virtual fruits if their hands are positioned at the correct places.

## Results
Our final product was a successful proof of concept game where basic game functions and the game controller were implemented, but did not have a completed UI. When players moved their hands, the cursor would move, and if the cursor overlapped the fruits they disappeared. Our game also featured basic physics where fruits were "tossed" onscreen, and fell out of the screen due to gravity. It also had basic sound effects for sliced fruits.

(include game screenshots)

## Implementation
We used the model-view-controller construction to create this game

#### Model:
Our game had a fruit object and a hand object. Fruits had a particular coordinate which was updated by effects from its initial velocity and gravity, and are created with a random size and speed based on parameters that were set to create an adequate difficulty for the game. The hand's coordinates were set to the output of the controller's corrdinates. If the coordinates of the hand overlapped the area of the fruit, then the fruit was "sliced."

#### View:
Each fruit object was a colored circle centered around the current coordinates of the fruit. The hand was represented with a small white circle so players could know where their hands were in-game. 

#### Controller:
For each frame in a webcam feed, the image is blurred and a mask is applied to create a binary image in which only colors in a particular color range (for which we used skin colors) are white and the rest is black. The largest continuous white area in the binary image is considered to be the hand, and the script computes the center of the hand based on this area. It passes the coordinates of the center to the model.

#### Integration:
The model, view, and controller aspects of our game all had to be repeatedly updated based on the camera input, so all three were integrated into the same while loop. During each loop, the game checked the webcam feed to obtain coordinates of the hand, checked to see if there were any collisions between the hand coordinate and a fruit, then updated the game by deleting "sliced" fruits and moving the intact ones. 

## Reflection
Our process went well-along the way - we had a minimum, reasonable, and reach goal for our project, which we agreed on the day the project was assigned. While doing the project, we regularly checked-in to make sure that both of us were on the same page about which product the project was going to be based on what seemed attainable given our current status. We ended up meeting our reasonable project goal, so overall it was fairly well scoped. 

As a team, we took on a divide-and-conquer approach while being available for help both ways if either of us got stuck. To meet our individual learning goals, Amy took on the OpenCV side of the project while Sid mostly worked on the model-view-controller side of the project. One issue that arose was the different setup we both had on our computers, so it took a bit to make sure the code we both wrote was compatible and could run on both of our laptops. We resolved this by taking the time to check the different versions of software we each had installed and made sure the ones we were going to use on this project worked and were properly set up on both computers. Next time, we'd probably check the versions before starting the project instead of trying to make it work mid-way through the project when code was already partially written for both versions. 
