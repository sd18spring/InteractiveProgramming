# Things to keep in mind when programming game
@author Corey Cochran-Lepiz & Nathan Estill

### Objects
1. Player
   * Needs to receive movement
   * Needs to shoot projectile
2. Arena
   * Doesn't actually end. Loops on itself (boundless but finite)
3. HUD
   * High score and # of lives left
4. Projectile
5. Asteroid
   * Small, Medium, and Large
6. UFO
   * Small, and Large

### Notes
1. Asteroids spawn  
   * Asteroids kill all
     * Except for themselves
   * Float through each other
2. Player can shoot self
   * Careful about spawning. Don't want to spawn into an asteroid
3. Asteroid speed
   * Gets faster after breakup
4. Number of asteroids/level???
5. Projectile
   * Travels ~3/4 of map length
6. Collision!
   * UFO wins against player
   * Player and asteroid lose together
   * UFO and asteroid lose together
7. BIG UFO
   * Travels from one side to the other
   * Down diagonally then up until out of play space
8. Smol UFO
   * One side to other in straight line

### Points!
Large asteroid = 20  
Medium asteroid = 50  
Smol asteroid  = 100  
BIG UFO = 200  
smol UFO = 1,000  
Life +1 after 10,000  
