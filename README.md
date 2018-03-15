# Interactive Programming
This is the base repo for the interactive programming project for Software Design, Spring 2018 at Olin College.

You need to install OpenCV for this project. Run this line to install: `$ pip install opencv-python`

#### To run the program
To run the program, please either download zip or type in `git clone https://github.com/Tweir195/InteractiveProgramming.git` in the command line. To run the program, please type `python main.py` in the command line.

Our program allows for three different modes, which you can specify through the few additional commands in the command line:

`-t`: The trailing mode where the line you control is of fixed length, so older points after a certain number of new points are drawn will disappear. This is the default mode in which the program will run.

`-g`: The gaming mode in which you try to hit colored boxes and get scores and added length to your line upon hittng the boxes.

`-l` or `--length`: An integer following this command will specify the starting length of the line in the trailing mode and the gaming mode. The default starting length is 3.

`-d` or `--draw`: The drawing mode where the line you control will stay on the screen as long as you haven't quit.

When the program is running, there are several keyboard interactions that you can use: Key `q` would allow you to quit the program; key `s` would allow you to save the current canvas; key `t` would allow you to toggle trailing ON or OFF.

## Project Overview
In this interactive programming project, we created a program that uses OpenCV to track a red object and makes up a drawing app by drawing in a canvas where the red object has been. There are a few modes that you can choose from: a game, a drawing canvas, and a canvas with a disappearing line.

## Results
The most basic function of our program is to draw a tailing line. Our program would first filter out the color red in the whole camera frame. After identifying the contour in the filtered red frame, the program records the coordinate of the center of contours as a point to draw lines with. In the end, we would have a list of such points. By drawing a line between every two consecutive points in the list, we would end up with the trajectory of the red object in the frame. The way we maintain the list is by appending new points to the list until the designated length has been reached and then just shifting out the first element in the list and appending the new point to the list.

![alt text](https://github.com/Tweir195/InteractiveProgramming/blob/master/drawing.jpg)

At the same time, there's the option to make all the points stay on the canvas. To implement this, the only slight variation is that we would keep appending the coordinates to the list of all the points instead of shifting out the first one every time.

![alt text](https://github.com/Tweir195/InteractiveProgramming/blob/master/gaming.jpg)

The gaming mode is just a step up from the simple trailing mode. When the gaming mode is enabled, the canvas class would place a randomly colored rectangle at a random location inside canvas. Upon a point falling inside the drawn rectangle, users will be given ten points, and the tail of the line will be made longer. The current rectangle disappears while a new one shows up at another randomly chosen location. At the start of the program, the current time of the program is also recorded. When a countdown from 30 finishes, the program will freeze gaming and display the scores that the user receives in this round.Whenever one second elapses, the countdown in the game mode will decrease by one.

## Implementation: still needs a UML
Our program includes two classes: `canvas` and `fingerTrack`.  The `canvas` class creates a canvas to be drawn on. The initialization of `canvas` involves three input parameters: the width of the canvas, the height, and the scaler to enlarge the canvas by. The width and the height are based off the size of the camera frame. The scaler is always 2 except in the gaming mode where a scaler of 1 is applied to allow for better accuracy when playing the game. The `fingerTrack` class performs color tracking and actual drawing on the canvas. Each location of the points to be drawn are also scaled with the scaler in the `canvas` class. It also takes the `canvas` class as an input parameter when drawing new points and lines.

The number of coordinates that a list is allowed to have before shifting out the first element is increased by 1.
Whenever one second elapses, the countdown in the game mode will decrease by one.

In our beginning planning of the project, after we had decided on using OpenCV to make a drawing platform, we had a few options. We thought about trying to make a game similar to the snake game, but the snake was controlled by the web-cam on the computer. We also thought about just making a canvas on the screen that could be drawn on by the web-cam, and have the color be controlled by the speed of movement. We were unsure about how easily we would be able to make the snake game, and decided on making the drawing canvas. However, we finished this with plenty of time, and expanded into a game in addition to the drawing canvas.

## Reflection
One thing that would have helped us a lot was having a more appropriately scoped project that takes better advantage of classes. We ended up doing a cool project, but because we started in an easier project, we had to keep finding ways to expand. This made us experiment with the code, without realizing we should have made a separate class for each mode.

One of the good things about the experience is that we both pair programmed and divide-and-conquer in the process. Our approach in dividing and conquer were based on the next tasks that need to get done instead of which files or classes specifically so that both us have a good understanding of the program as a whole. We were able to move along in the project quite steadily, not feeling stressed about not feeling our project.

### Our initial project proposal can be found [here](https://github.com/QingmuDeng/InteractiveProgramming/blob/master/Project%20Proposal.md).
