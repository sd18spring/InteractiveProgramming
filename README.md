# Virtual Music Board
Software Design Mini-Project 4 (Spring 2018) code and documentation.

## Overview
In this project, we aimed to make a “note board” that the user can play in a variety of different ways.
This “note board” is essentially a musical keyboard with twelve notes (Ab to G). We wanted the user to
be able to operate the note board with a mouse, with their computer keyboard, or with their body.
Mouse and keyboard operation would be through event detection and body operation would be using
computer vision to detect body location.

## Getting Started
To get the keyboard up and running, please update your Linux dependecies:

```
sudo apt-get update
sudo apt-get upgrade
```

Libraries used:

* [OpenCV](https://docs.opencv.org/2.4.9/modules/refman.html) for computer-vision based controls
* [Sonic-Pi](http://sonic-pi.net/) for music notes
* [PyGame](http://www.pygame.org/docs/) for creating the keyboard layout
* [NumPy](https://docs.scipy.org/doc/numpy/reference/index.html) to create a matrix of zeroes
* [OS](https://github.com/python/cpython/blob/3.6/Lib/os.py) for reading the .wav files

Installing the libraries:

```
apt search opencv
sudo apt-get install libopencv
pip install opencv-python

sudo add-apt-repository ppa:sonic-pi/ppa
sudo apt-get update
sudo apt-get install sonic-pi
pip install python-sonic

sudo apt-get build-dep python-pygame
sudo apt-get install mercurial python-dev python-numpy ffmpeg libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libsdl1.2-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
pip install pygame
```
_NumPy_ and _OS_ are standard Python libraries which should be pre-installed on computers running Linux.  

## Deployment
To run the code, we first need to run Sonic-Pi program on our machines. Test if Sonic-Pi is working properly by typing the following command in the Sonic-Pi terminal:`play 60`.

Please hit _Run_ after this. If you hear a beep then you're all set. If not, then please try to re-install Sonic-Pi. After this, please type the following command into the Sonic-Pi terminal and _Run_ the terminal again: 
```
play 60
set_sched_ahead_time! 0
```

You should hear another beep this time. These commands will make sure that there is no delay while playing the notes on the keyboard.

Next, choose the file you want to run. [computer_vision_note_board.py](https://github.com/Utsav22G/InteractiveProgramming/blob/master/computer_vision_note_board.py) uses OpenCV to track the movement of an object, like your hand or your head, and play the notes accordingly. [mouse_keyboard_note_board.py](https://github.com/Utsav22G/InteractiveProgramming/blob/master/mouse_keyboard_note_board.py) uses the _QWERTY_ row of your keyboard and the your mouse buttons to play the notes.

### NOTES
* You will need a working webcam to run _computer_vision_note_board.py_. Optimum distance for _computer_vision_note_board.py_ is about 1.5 to 2 feet. Please don't come too close or move too far away from your webcam.
* To exit out of the program, you'll first need to close the Sonic-Pi program window and then close the PyGame keyboard layout window. 

## Authors
[Utsav Gupta](https://github.com/utsav22g) and [Julian Stone](https://github.com/JulianStone5)

## Acknowledgement
Thanks to the awesome NINJAs Matt, Vicky and Nina, and the amazing teaching team for their guidance and support!
