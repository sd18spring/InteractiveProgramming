# Project Reflection
### Authors: Corey Cochran-Lepiz, Nathan Estill

## Project Overview [max 100 words]

We created a Pygame version of the classic arcade game, Asteroids.

## Results [~2-3 paragraphs + figures/examples]

We ended up with a game that does a good job resembling the original game. The player starts with three lives. They have a ship that moves with an acceleration and turning based system. The ship slows down when not accelerating and can "drift" when turning while going forward. Colliding with asteroids or UFOs, or getting hit by the UFOs projectile makes the player lose a life. The ship shoots a projectile that goes about 5/8 of the size of the screen. Hitting other objects with the ship's projectiles grants points depending on the object. No other interactions grant points. For every 10000 points the player receives, another life is granted.

The asteroids spawn in random places around the map and break up when hit with a non-asteroid object. They break up twice into two more smaller asteroids and disappear on the third hit. Large asteroids are worth 20 points, medium asteroids are worth 50 and small asteroids are worth 100. The UFOs spawn randomly throughout the game. They move in either a straight line or a in a up and down fashion. They shoot in random directions at a distance that is lower than that of the Ship's projectiles. UFOs can shoot asteroids and hit asteroids, but does not grant points if destroyed in this manner. The UFO is worth 500 points.
![A screen shot of the game working](FullGame.png)

## Implementation [~2-3 paragraphs + UML diagram]
Our implementation for the non-controllable objects consisted of making a class for each object. Each class had an update function that handled the movement of the object and a destroy function, for when the object was destroyed. The asteroid and UFO had subclasses that inherited them, one for each size of asteroid, and one for each type of asteroid (We had initially planned to add a second type of UFO, but ran out of time). Each of these classes had an overarching class that contained all of the instances of the lower class. This made collision detection much easier and allowed us to simply update the greater class, which in turn updated all of the instances. There was one class that contained all of the objects in the game, holding the overarching classes for each object. This class handled collision detection and updated all of the objects.

Class Diagram
* listOfObjects - contains and keeps track of all objects
  * listOfAsteroids - contains and keeps track of all asteroids
    * Asteroid - Base Asteroid class
      * Small Asteroid - Inherits from Asteroid
      * Medium Asteroid - Inherits from Asteroid
      * Large Asteroid - Inherits from Asteroid
  * listOfUFOs - contains and keeps track of all UFOs
    * UFO - Base UFO class
      * BigUFO - Inherits from UFO
      * SmallUFO (not implemented) - Inherits from UFO
  * listOfProjectiles - contains and keeps track of all Projectiles
    * Projectile - Base Projectile class
  * Ship
## Reflection [~2 paragraphs]


Please prepare a short document (~1 page not including figures) with the following sections:

Project Overview [Maximum 100 words]

Write a short abstract describing your project.

Results [~2-3 paragraphs + figures/examples]

Present what you accomplished. This will be different for each project, but screenshots are likely to be helpful.

Implementation [~2-3 paragraphs + UML diagram]

Describe your implementation at a system architecture level. Include a UML class diagram, and talk about the major components, algorithms, data structures and how they fit together. You should also discuss at least one design decision where you had to choose between multiple alternatives, and explain why you made the choice you did.

Reflection [~2 paragraphs]

From a process point of view, what went well? What could you improve? Other possible reflection topics: Was your project appropriately scoped? Did you have a good plan for unit testing? How will you use what you learned going forward? What do you wish you knew before you started that would have helped you succeed?

Also discuss your team process in your reflection. How did you plan to divide the work (e.g. split by class, always pair program together, etc.) and how did it actually happen? Were there any issues that arose while working together, and how did you address them? What would you do differently next time?
