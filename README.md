### Our initial project proposal can be found [here](https://github.com/QingmuDeng/InteractiveProgramming/blob/master/Project%20Proposal.md).
### Our project reflection can be found [here](https://github.com/Tweir195/InteractiveProgramming/blob/master/ProjectReflection.md).

You need to install OpenCV for this project. Run this line to install: `$ pip install opencv-python`

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
