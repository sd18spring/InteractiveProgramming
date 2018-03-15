# Interactive Programming
This is the base repo for the interactive programming project for Software Design, Spring 2018 at Olin College.

You need to install OpenCV for this project. Run this line to install: `$ pip install opencv-python`

## Project Overview
In this interactive programming project, we created a program that uses OpenCV to track a red object and makes up a drawing app by drawing in a canvas where the red object has been.

#### To run the program
To run the program, please either download zip or type in `git clone https://github.com/Tweir195/InteractiveProgramming.git` in the command line. To run the program, please type `python main.py` in the command line.

Our program allows for three different modes, which you can specify through the few additional commands in the command line:

`-t`: The trailing mode where the line you control is of fixed length, so older points after a certain number of new points are drawn will disappear. This is the default mode in which the program will run.

`-g`: The gaming mode in which you try to hit colored boxes and get scores and added length to your line upon hittng the boxes.

`-l` or `--length`: An integer following this command will specify the starting length of the line in the trailing mode and the gaming mode. The default starting length is 3.

`-d` or `--draw`: The drawing mode where the line you control will stay on the screen as long as you haven't quit.

When the program is running, there are several keyboar d interactions that you can use: Key `q` would allow you to quit the program; key `s` would allow you to save the current canvas; key `t` would allow you to toggle trailing ON or OFF.

## Results


## Implementation: still needs a UML
Our program include two classes: `canvas` and `fingerTrack`.  Whereas the `canvas` class create a canvas to be drawn on and update the canvas, `fingerTrack` performs color tracking and actual drawing onto the canvas.

The most basic function of our program is to draw a tailing line. Our program would first filter out the color red in the whole camera frame. After identifying the contour in the filtered red frame, the program records the coordinate of the center of contours as a point to draw lines with. In the end, we would have a list of such points. By drawing a line between every two consecutive points in the list, we would end up with the trajectory of the red object in the frame. The way we maintain the list is by appending new points to the list until the designated length has been reached and then just shifting out the first element in the list and appending the new point to th list.

At the same time, there's the option to make all the points stay on the canvas. To implement this, the only slight variation is that we would keep appending the coordinates to the list of all the points instead of shifting out the first one every time.

The gaming mode is just a step up from the simple trailing mode. When the gaming mode is enabled, the canvas class would place a randomly colorred rectangle at a random location inside canvas. Upon a point falling inside the drawn rectangle, users will be given ten points, and the number of coordinates that a list is allowed to have before shifting out the first element is increased by 1. The current rectanlge disappears while a new one shows up at another randomly chosen location. AT the start of the program, the current time of the program is also recorded. Whenever one second elapses, the counterdown in the game mode will decrease by one. When the countdown finishes, the program will freeze gaming and display the scores that the user receives in this round.

## Reflection



### Our initial project proposal can be found [here](https://github.com/QingmuDeng/InteractiveProgramming/blob/master/Project%20Proposal.md).
