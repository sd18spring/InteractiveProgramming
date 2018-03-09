# Mid-Project Check-In

## Sound from Interactive Drawing by Jane and Lydia

### Current Overview

So far, we have tested sound playback using pygame and have made a lot of progress in our code for interactive drawing. We have determined that pygame is capable of doing what we want in terms of sound, and we know one method which we can use to fulfill that need. We have also gotten to the point with our drawing code that the user can fill in squares in a grid with different shapes and colors using their mouse.

Going forward, we are working on implementing a radial sweep in the drawing that will generate a dictionary of the grid points around where you click in circles of increasing size. Meaning, you will be able to click on the grid at some point, and the program will look at larger and larger circles with their centers at the point you clicked, and will generate a list of points on each circle that you have drawn in. In the future, this will allow us to play sound based on the location, shape, and color of the points the user has drawn in. We will most likely create a separate code file for the sound playback, then import it into the drawing code for use. At this point in time, we plan to have the sound chosen for each note determined as follows:

*Shape: Note vs. Chord*

*Fill: Short vs. Sustained*

*Color: Instrument/Sound Type*

*Angle on the Circle: Pitch (i.e., top pizza = C, bottom pizza = F)*

### Next Steps

- Generate sweeper class that will sweep the aforementioned circles.
- Add ability to look at the blocks in a ring and choose sounds based on them
  - Create dictionaries of block qualities => sound properties
  - Determine angle of sound block relative to start point
  - Add a LOT of sound files!
- Play sounds in a ring all at once, rings one after another
- Add buttons for UI (optional but preferred)
