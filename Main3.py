import pygame
import time
import random
import cv2
import numpy as np

display_width = 800
display_height = 600
white=(0,255,255)
black=(0,0,0)

# barImg = pygame.image.load('spielfigur.png')
barImg = pygame.image.load('Genie1.png')
bomb1=pygame.image.load('bomb1.png')
bomb2=pygame.image.load('bomb2.png')

bar_width = 20

def bar(x, y):
   gameDisplay.blit(barImg, (x, y))


def game_loop():


   x = (display_width * 0.5)
   y = (display_height * 0.8)
   x = 0

   x_start = random.randrange(0, display_width)  ##Where the moving blocks start moving from
   y_start = -200  ## Object starts 600 pixels above the window
   moving_block_speed = 7  # Determines the speed at which the object moves
   width = 100
   height = 100
   radius = random.randrange(100, 200)

   gameExit = False
   crashed = False

   while not gameExit:

       ret, frame = cap.read()
       faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20, 20))

       for (x, y, w, h) in faces:
           cv2.circle(frame, (w / 2 + x, h / 2 + y), 10, (255, 255, 255), -1)

       # for event in pygame.event.get():
       #     if event.type == pygame.QUIT:
       #         gameExit = True
       #     if event.type == pygame.KEYDOWN:
       #         # print("3")
       #         if event.key == pygame.K_LEFT:
       #             # print("4")
       #             x_change = -5
       #         elif event.key == pygame.K_RIGHT:
       #             # print("5")
       #             x_change = 5
       #     if event.type == pygame.KEYUP:
       #         if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
       #             x_change = 0

       print x
       x = (float)(x)/ (365) * 800
       if (x >600):
           x = 780
       print x
       print (" ")

       gameDisplay.fill(white)

       choice = random.randrange(0, 3)

       if choice==1:
           gameDisplay.blit(bomb1,(x_start,y_start))
       else:
           gameDisplay.blit(bomb2, (x_start,y_start))
       y_start += moving_block_speed

       if x >= display_width - bar_width:
           x = display_width - bar_width
       if x < 0:
           x = 0

       if y_start > display_height:
           y_start = 0 - height
           x_start = random.randrange(0, display_width)

       # bar(800-x, 500)
       if crashed == False:
           bar(x, 500)
       else:
           break

       if 460 <= y_start <= 540 and x - 50 <= x_start <= x + 100:
           crashed = True

       if crashed == True:
           moving_block_speed = 0
           y_start = 420

       pygame.display.update()
       clock.tick(60)

       time.sleep(.01)

       cv2.imshow('frame', frame)
       if cv2.waitKey(1) & 0xFF == ord('q'):break

if __name__ == '__main__':
    pygame.init()  # Initially sets the window after predefining some colors and setting the pygame window specs
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Image Controlled Game')
    clock = pygame.time.Clock()

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    kernel = np.ones((40, 21), 'uint8')
    cap = cv2.VideoCapture(0)

    game_loop()
    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()
