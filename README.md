# InteractiveProgramming
This is the base repo for the interactive programming project for Software Design, Spring 2018 at Olin College.

#Dependencies
You need to install: wikipedia, pygame, bs4
Other libraries used: urllib, math, collections, string
wiki_functions.py was written by Aiden Carley-Clopton as par of MP2

#Use
To run the code, run $ python wikipedia_visualizer.py

Click on the rectangle and type in the title of the article you want ot start at.
Hit enter to generate the first node. Click on it to expand it and find the first
few links (the default value is 3, and can be changed by pressing one of the number
keys). Right click on a node to open the wikipedia page in your browser. Zooming
happens with new node generation and can be done manually by scrolling,panning is
 done by dragging with left click held down.

If you want to delete a branch, hover over a node and press the delete key to delete
all of it's children. If you click on the node again, you'll get a new set of links
to explore.

Hitting the 'd' key while not in the search bar will expand every node one layer.
This is good for building a tree, but I should warn you it takes a while (since
the program has to search the internet for results)

Hitting the 's' key while not in the text box will save the current tree to a file.
To load a file, type the name ending in '.txt', and the code will parse it. If the file
doesn't exist, it just won't load anything. I've included the examples 'philosophy.txt',
'metal.txt','box.txt', and 'eigen vector.txt' so you can load them and take a look.
Note that deletion is not fully supported in files generated from saves.

Screenshots of use can be found in /screenshots
