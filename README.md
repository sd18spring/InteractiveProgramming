# InteractiveProgramming: Cat Map
This is for the interactive programming project for Software Design, Spring 2018, at Olin College.

Cat Map is an interactive visualization of hurricane data within the NOAA database. The data is obtained by accessing csv files stored in a FTP server. Various hurricane paths are plotted on a map that users can easily zoom into and explore. The points and paths are color coded according to the category of the hurricane. Additional features include a slider for year that determines which hurricanes are plotted and a hover window that is generated for every point in a hurricane path. The hover includes the name, time, duration, and category for a given hurricane. 

The structure of our program involves object-oriented programming. The Map.py file creates a Model object, which in turn creates a bunch of Hurricane objects, and combines the data with interactive components from Bokeh. 

To initiate the Cat Map, type __"bokeh serve --show Map.py"__ into the terminal. The map needs to be generated using the bokeh server. Additionally, you many need to install several support libraries for the program to execute. The following is a list of python libraries that are utilized with installation instructions:
- pickle (comes with Python)
- [pandas](https://pandas.pydata.org/) 
- [bokeh](https://bokeh.pydata.org/en/latest/docs/installation.html) 
- numpy ("pip install numpy")
- datetime ("pip install datetime")
- Additional libraries that don't need to installed to run map (used for data.py)
  - [splinter](http://splinter.readthedocs.io/en/latest/install.html)
  - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) 
  - time (comes with Python)

A more detailed description of our project can be found [here](https://www.goodreads.com).

If you have any questions, please contact us at cassandra.overney@students.olin.edu and elizabeth.tawes@students.olin.edu.
