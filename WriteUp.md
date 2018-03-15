# Project Overwiew
Our project is a data visualizer for movie ratings. It displays each movie as a dot with a color gradient that represents
the ratio of critic movie ratings to user movie ratings. When a dot is clicked on it displays individual dots for the movie,
but now each dot represents the data from one movie rating website.

# Results
The "home screen" of our project displayes about 148 dots, each of which represents a single movie. Each of these dots are
layed out on the home screen in the shape of a circle, essentially creating a giant dot with all of the movie dots. The color of
each dot represents the ratio of the critic to user rating of the given movie. A more blue dot signifies that the movie
had a higher critic score than a user score and vice versa for a more pink/red colored dot.

When the user clicks on a single dot, an animation of zooming in on that dot plays and it is split into its subdots which posess
the same qualities as the dots on the "home screen" excpet now the color gradient is for each individual movie-rating website
(Rotten Tomato and Metacritic). When in this zoomed in state, if the user clicks anywhere on the screen, the program will return
to the home screen, and the user can, again, click on any dot to repeat the experience.

## Home
![home](https://user-images.githubusercontent.com/15020544/37495712-fcb5c190-2884-11e8-9644-623bcb7e13d5.png)

## Animation
![animation](https://user-images.githubusercontent.com/15020544/37495738-1f115362-2885-11e8-9f7d-ce6d230a3471.png)

## Subdots
![subdots](https://user-images.githubusercontent.com/15020544/37495757-37c9350a-2885-11e8-8527-00b01451b1e2.png)

# Implementation
First we creted a MovieDot class which inherits from the Dot class and stores a label (movie name) and movie (data about that
movie). The movie attribute of MovieDot is another class as well. MovieDot bridges the Dot and Movie classes. When the program first
runs all the "home screen" dots are added to a list and an algorithm we used minmized collisions between dots when they are randomly
placed within the area of a predetermined circle. Dots are only appended to the list when they are a sufficient distance away from other
dots. Moreover, one dot is predetermined so that the second and rest have something to be compared to. 

When a dot is clicked on, the animation is dont using a deep copy of the home dots which are stored in their own list so that the original home dots are not
modified. A dictionary was also made which contain the name of a movie as the key and the instances of its MovieDot children as its
values. Then the children are assigned to the original dots list so that the original draw function does not have to be changed. We simply
changed the data it accesses. These list are switched back when the user returns to the "home screen."

In order to represent the value of the color, the movie rating data was rescaled to an RGB color where the R value represents the critic score,
the B represents the user score, and the G is always zero so that the gradient always ranges between red and blue. This was achieved
with the remapping equation: 

V' = ((v - min) / (max - min)) * (newMax - newMin) + newMin.

One design decision we made in this project was to use a boolean to determine when the model was in a zoomed in state instead of
making two functions (one to zoom in AND out). In this manner it kept the rest of the function the same because all we did was switch the data in their structures, rather
than making new methods to deal with the new state.

## UML Diagram
![uml](https://user-images.githubusercontent.com/15020544/37495810-8822d7a4-2885-11e8-8926-175cdd8073c3.jpg)

# Reflection
What went well in this project was the way that we divided the work. Hyegi wanted to do data manipuation and visualization, and I (Mark) wanted
to develop the user interface. Because of this, we were able to work on our seperate parts and then easily merge them together when we were both together.
We could have improved on our collaboration frequency throughout the project and communicated more about the status of what we were working on.
We think that our project was appropriatly mostly scoped appropriatly because our initial MVP was more challenging than we expected it to be. So, we
ended up scaling it down a little and not achieving as much of our stretch goals as we intially intended to (such as creating a gradient with all the dots on the "home screen" or representing gross revenue with radius size). We will make sure that the project
is appropriatly scoped before moving foward with its creation. We will also come up with concrete stretch goals to extend the project. We wish we knew of the
technique of using index as a parameter of a class that stores data in order to retrieve the correct data. This was a major road block, in assigning movies to dots, and would
have saved us A LOT of time. In terms of partnering, next time we'd want to, as stated above, communicate more with our partner.

