
# coding: utf-8

# In[1]:


import pygame
import random

class keys:
    def __init__(self, event= None):
        self.last_pressed = ""
        self.string = "Pressed:"
        if event.key == pygame.K_UP:
            self.UP = True
            self.string += "UP"
        else:
            self.UP = False
        if event.key == pygame.K_DOWN:
            self.DOWN = True
            self.string += "DOWN"
        else:
            self.DOWN = False
        if event.key == pygame.K_RIGHT:
            self.RIGHT = True
            self.string += "RIGHT"
            self.last_pressed = "RIGHT"
        else:
            self.RIGHT = False    
        if event.key == pygame.K_LEFT:
            self.LEFT = True
            self.string += "LEFT"
            self.last_pressed = "LEFT"
        else:
            self.LEFT = False 
 
    def __str__(self):
        return self.string
        
        
def xy_position_to_pixels(Rectangle, window_size, virtual_window):
    """Takes:In-game coordinate rectangle
    Converts in game coordinates to pixels. Also, note that the in-game position refers to the LOWER RIGHT hand
    corner of the sprite. 
    Returns: rectangle in pixel coordinates"""
    x = Rectangle[0]
    y = Rectangle[1]
    width = Rectangle[2]
    height = Rectangle[3]
    pixel_x = int(float(x/virtual_window[0])*window_size[0])
    pixel_y = window_size[1] - int(float(y/virtual_window[1])*window_size[1])
    pixel_width = int(float(width/virtual_window[0])*window_size[0])
    pixel_height = int(float(height/virtual_window[1])*window_size[1])
    pixel_y -= pixel_height
    return (pixel_x, pixel_y, pixel_width, pixel_height)



class position:
    def __init__(self, current_x = 0, current_y = 0, current_xs = 0, current_ys = 0, floor = 0, button=None,
                character_width = 30, character_height = 30, wall_speed = .3):
        self.current_x = current_x
        self.current_y = current_y
        self.current_xs = current_xs
        self.current_ys = current_ys
        self.button = button
        self.floor = floor
        self.last_pressed = None
        self.jump = False
        self.character_width = character_width
        self.character_height = character_height
        self.wall = None
        self.wall_speed = wall_speed
        self.maintain = False
        
    def __str__(self):
        return str(self.current_x)+" "+str(self.current_y)+" "+str(self.current_xs)+" "+str(self.current_ys)
    
    def give_next_position(self, floor, wall): #fix button 
        #print("The give next position function has run.")
        #print("Button:", button)
        self.floor = floor
        self.wall = wall
        
        
        if self.current_y <= self.floor:
            self.current_ys = 0
            self.jump = False
        if not self.jump:    
            self.current_xs = -1*self.wall_speed
        if self.current_y > self.floor:
            self.current_ys -= .3
            
        if self.button != None: 
            #print("AH I SENSE MOVEMENT!")
            if self.current_y == self.floor:
                if self.button.UP:
                    pygame.mixer.Sound.play(jump_sound) #HERE
                    self.current_ys = 7
                    if self.last_pressed == "RIGHT":
                        self.current_xs = 1
                        self.jump = True
                        if wall[1] != None:
                            if self.current_x+self.character_width+1 >= wall[1]:
                                self.current_xs = 0
                    elif self.last_pressed == "LEFT":
                        self.current_xs = -1 - self.wall_speed
                        self.jump = True
                        if wall[0] != None:
                            if self.current_x <= wall[0]:
                                self.current_xs = 0
                        
            if self.button.RIGHT:
                self.current_xs = 1
                if wall[1] != None:
                    if self.current_x+self.character_width+1 >= wall[1]:
                        self.current_xs = 0
            elif self.button.LEFT:
                self.current_xs = -1 - self.wall_speed
                if wall[0] != None:
                    if self.current_x <= wall[0]:
                        self.current_xs = 0
            self.last_pressed = self.button.last_pressed
        
        self.current_x += self.current_xs
        self.current_y += self.current_ys
        
        #collision effects
        if wall[0] != None:
            if self.current_x <= wall[0]:
                self.current_x = wall[0]+1
        
        if wall[1] != None:
            
            #print("I am at x position ", str(self.current_x+self.character_width))
            
            if self.current_x+self.character_width >= wall[1]:
                self.current_x = wall[1]-self.character_width-1
                
            if self.current_x+self.character_width+1 >= wall[1]:
                    self.current_x -= self.wall_speed
        
        if self.current_y < self.floor:
            self.current_y = self.floor
        


# In[2]:


###PLATFORMS###
class platform:
    def __init__(self, x1, x2, height):
        self.leftX = x1
        self.rightX = x2
        self.height = height

platform_generation_list = [(120,200,50)]

def generate_list_of_platform_objects(platform_generation_list):
    list_of_platforms = []
    for i in platform_generation_list:
        platform_temp = platform(i[0], i[1], i[2])
        list_of_platforms.append(platform_temp)
    return list_of_platforms

def generate_list_of_platforms_on_screen(list_of_platforms, virtual_window):
    list_of_platforms.sort(key = lambda plat: plat.leftX) ###SORT BY LEFTX
    list_of_platforms_on_screen = []
    for i in list_of_platforms:
        if i.rightX < 0:
            continue
        list_of_platforms_on_screen.append(i)
        if i.leftX > virtual_window[0]:
            break
    return list_of_platforms_on_screen

def blit_platform(platform, window_size, virtual_window):
    rectangle = (platform.leftX, platform.height - 5, platform.rightX-platform.leftX, 5)
    pixel_rectangle = xy_position_to_pixels(rectangle, window_size, virtual_window)
    screen.blit(texture_scaled,pixel_rectangle,pixel_rectangle)
    
    contrast_rectangle = (platform.leftX, platform.height - 3, platform.rightX-platform.leftX, 2)
    pixel_contrast_rectangle = xy_position_to_pixels(contrast_rectangle, window_size, virtual_window)
    pygame.draw.rect(screen,(212, 78, 77),pixel_contrast_rectangle)
    
    icing_rectangle = (platform.leftX, platform.height - 2, platform.rightX-platform.leftX, 2)
    pixel_icing_rectangle = xy_position_to_pixels(icing_rectangle, window_size, virtual_window)
    pygame.draw.rect(screen,(255, 205, 205),pixel_icing_rectangle)
    
    


###BLOCKS###
class block:
    def __init__(self, x, y, width, height):
        self.leftX = x
        self.rightX = x+width
        self.height = y + height
        self.bot = y
        self.text = "(" + str(x)+ ", " + str(y)+ ", " + str(width)+ ", " + str(height)+")" 
        

def generate_list_of_block_objects(block_generation_list):
    list_of_blocks = []
    for i in block_generation_list:
        block_temp = block(i[0],i[1], i[2], i[3])
        list_of_blocks.append(block_temp)
    return list_of_blocks

def generate_list_of_blocks_on_screen(list_of_blocks, virtual_window):
    list_of_blocks.sort(key = lambda bl: bl.leftX) ###SORT BY LEFTX
    list_of_blocks_on_screen = []
    for i in list_of_blocks:
        if i.rightX < 0:
            continue
        list_of_blocks_on_screen.append(i)
        if i.leftX > virtual_window[0]:
            break
    return list_of_blocks_on_screen

def blit_block(block, window_size, virtual_window, font):
    rectangle = (block.leftX, block.bot, block.rightX-block.leftX, block.height-block.bot)
    pixel_rectangle = xy_position_to_pixels(rectangle, window_size, virtual_window)
    screen.blit(texture_scaled,pixel_rectangle,pixel_rectangle)
    
    shadow_rectangle = (block.leftX,block.height-4, block.rightX-block.leftX, 2)
    pixel_shadow_rectangle = xy_position_to_pixels(shadow_rectangle, window_size, virtual_window)
    pygame.draw.rect(screen,(226, 168, 85), pixel_shadow_rectangle)
    
    contrast_rectangle = (block.leftX,block.height-3, block.rightX-block.leftX, 2)
    pixel_contrast_rectangle = xy_position_to_pixels(contrast_rectangle, window_size, virtual_window)
    pygame.draw.rect(screen,(212, 78, 77), pixel_contrast_rectangle)
    
    icing_rectangle = (block.leftX-2,block.height-2, block.rightX-block.leftX+2, 2)
    pixel_icing_rectangle = xy_position_to_pixels(icing_rectangle, window_size, virtual_window)
    pygame.draw.rect(screen,(255, 205, 205), pixel_icing_rectangle)
    
    #textsurface = font.render(block.text, False, (0, 0, 0))
    #xy_position_of_text = (pixel_rectangle[0],pixel_rectangle[1])
    #screen.blit(textsurface,xy_position_of_text)
    
def scroll_everything_left(list_of_platforms, list_of_blocks, list_of_badbreads, list_of_ingredients, world_speed):
    for platform in list_of_platforms:
        platform.rightX -= world_speed
        platform.leftX -= world_speed
    for block in list_of_blocks:
        block.rightX -= world_speed
        block.leftX -= world_speed
    for badbread in list_of_badbreads:
        badbread.startx -= world_speed
        badbread.endx -= world_speed
        badbread.current_bread_x -= world_speed
    for ingredient in list_of_ingredients:
        ingredient.ingredient_position_x -= world_speed 
        


# In[3]:


class badbread:
    def __init__(self, startx, starty, endx, speed = .5):
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.speed = speed
        self.current_bread_x = startx
        self.size = 40
    
    def move_badbread(self):
        if self.current_bread_x < self.startx:
            self.speed = abs(self.speed)
        if self.current_bread_x > self.endx:
            self.speed = -1*abs(self.speed)
        self.current_bread_x += self.speed

def generate_list_of_badbreads(badbread_generation_list):
    list_of_badbreads = []
    for i in badbread_generation_list:
        badbread_temp = badbread(i[0], i[1], i[2])
        list_of_badbreads.append(badbread_temp)
    return list_of_badbreads

def generate_list_of_badbreads_on_screen(list_of_badbreads, virtual_window):
    list_of_badbreads.sort(key = lambda bl: bl.startx) 
    list_of_badbreads_on_screen = []
    for i in list_of_badbreads:
        if i.endx+i.size < 0:
            continue
        list_of_badbreads_on_screen.append(i)
        if i.startx > virtual_window[0]:
            break
    return list_of_badbreads_on_screen

def blit_badbread(badbread, window_size, virtual_window):
    rectangle = (badbread.current_bread_x, badbread.starty, badbread.size, badbread.size)
    pixel_rectangle = xy_position_to_pixels(rectangle, window_size, virtual_window)
    if badbread.speed > 0:
        screen.blit(bread_right_scaled,pixel_rectangle)
    else:
        screen.blit(bread_left_scaled,pixel_rectangle)

def generate_badbread_collisions(list_of_badbreads_on_screen, list_of_badbreads, current_position):
    badbread_collisions = []
    current_position_rectangle = pygame.Rect(
        xy_position_to_pixels((current_position.current_x, current_position.current_y,
            current_position.character_width, current_position.character_height), virtual_window, window_size))
    for i in list_of_badbreads_on_screen:
        badbread_rectange = pygame.Rect(xy_position_to_pixels(
            (i.current_bread_x + 5, i.starty, i.size-5, i.size-10), 
            virtual_window, window_size))
        if current_position_rectangle.colliderect(badbread_rectange):
            if current_position.maintain == False:
                collision_temp = collision("badbread", 0)
                badbread_collisions.append(collision_temp)
                print("hit a badbread")
                current_position.maintain = True
        else:
            current_position.maintain = False
            #print("disengaged")
    return badbread_collisions
##HERE


# In[4]:


class ingredient:
    def __init__(self, ingredient_type, ingredient_position_x,ingredient_position_y, size = 20):
        self.ingredient_type = ingredient_type
        self.ingredient_position_x = ingredient_position_x
        self.ingredient_position_y = ingredient_position_y
        self.size = size
        
def generate_list_of_ingredients(ingredient_generation_list):
    list_of_ingredients = []
    for i in ingredient_generation_list:
        ingredient_temp = ingredient(i[0], i[1], i[2])
        list_of_ingredients.append(ingredient_temp)
    return list_of_ingredients

def generate_list_of_ingredients_on_screen(list_of_ingredients, virtual_window):
    list_of_ingredients.sort(key = lambda bl: bl.ingredient_position_x) 
    list_of_ingredients_on_screen = []
    for i in list_of_ingredients:
        if i.ingredient_position_x+i.size < 0:
            continue
        list_of_ingredients_on_screen.append(i)
        if i.ingredient_position_x > virtual_window[0]:
            break
    return list_of_ingredients_on_screen

def blit_ingredient(ingredient, window_size, virtual_window):
    if ingredient.ingredient_type == "milk":
        rectangle = (ingredient.ingredient_position_x, ingredient.ingredient_position_y, ingredient.size, ingredient.size)
        pixel_rectangle = xy_position_to_pixels(rectangle, window_size, virtual_window)
        screen.blit(milk_scaled,pixel_rectangle)
    elif ingredient.ingredient_type == "celery":
        rectangle = (ingredient.ingredient_position_x, ingredient.ingredient_position_y, ingredient.size, ingredient.size)
        pixel_rectangle = xy_position_to_pixels(rectangle, window_size, virtual_window)
        screen.blit(celery_scaled,pixel_rectangle)
    elif ingredient.ingredient_type == "chocolate":
        rectangle = (ingredient.ingredient_position_x, ingredient.ingredient_position_y, ingredient.size, ingredient.size)
        pixel_rectangle = xy_position_to_pixels(rectangle, window_size, virtual_window)
        screen.blit(chocolate_scaled,pixel_rectangle)
    elif ingredient.ingredient_type == "vanilla":
        rectangle = (ingredient.ingredient_position_x, ingredient.ingredient_position_y, ingredient.size, ingredient.size)
        pixel_rectangle = xy_position_to_pixels(rectangle, window_size, virtual_window)
        screen.blit(vanilla_scaled,pixel_rectangle)
    elif ingredient.ingredient_type == "flour":
        rectangle = (ingredient.ingredient_position_x, ingredient.ingredient_position_y, ingredient.size, ingredient.size)
        pixel_rectangle = xy_position_to_pixels(rectangle, window_size, virtual_window)
        screen.blit(flour_scaled,pixel_rectangle)
    elif ingredient.ingredient_type == "sugar":
        rectangle = (ingredient.ingredient_position_x, ingredient.ingredient_position_y, ingredient.size, ingredient.size)
        pixel_rectangle = xy_position_to_pixels(rectangle, window_size, virtual_window)
        screen.blit(sugar_scaled,pixel_rectangle)
    elif ingredient.ingredient_type == "butter":
        rectangle = (ingredient.ingredient_position_x, ingredient.ingredient_position_y, ingredient.size, ingredient.size)
        pixel_rectangle = xy_position_to_pixels(rectangle, window_size, virtual_window)
        screen.blit(butter_scaled,pixel_rectangle)


# In[5]:


def give_floor_value(current_position, blocks_on_screen, platforms_on_screen):
    list_of_floors_under = []
    for i in blocks_on_screen:
        if i.rightX < current_position.current_x+10:
            continue
        if i.leftX > current_position.current_x+current_position.character_width:
            break
        if i.leftX < current_position.current_x+current_position.character_width -10 and current_position.current_x < i.rightX:
            list_of_floors_under.append(i)
            
    for i in platforms_on_screen:
        if i.rightX < current_position.current_x+10:
            continue
        if i.leftX > current_position.current_x+current_position.character_width:
            break
        if i.leftX <= current_position.current_x+current_position.character_width-10 and current_position.current_x +10 <= i.rightX:
            list_of_floors_under.append(i)
    list_of_floors_under.sort(key = lambda structures: structures.height, reverse = True)
    if list_of_floors_under != []:
        list_of_floors_under.sort(key = lambda fl: fl.height, reverse = True)
        #print("y= ",current_position.current_y)
        for i in list_of_floors_under:
            if i.height <= current_position.current_y:
                #print("floor =",i.height)
                return i.height
    return -500

def give_wall_value(current_position, blocks_on_screen):
    level_with_character = []
    for i in blocks_on_screen:
        if i.bot > current_position.current_y+current_position.character_height: #HERE
            continue
        if i.height < current_position.current_y:
            continue
        level_with_character.append(i)
    closest_left = None
    closest_right = None
    if level_with_character != []:
        level_with_character.sort(key=lambda blocks: blocks.rightX)
        for i in level_with_character:
            if i.rightX-10 < current_position.current_x:
                closest_left = i.rightX-10
        level_with_character.sort(key=lambda blocks: blocks.leftX, reverse = True)
        for i in level_with_character:
            if i.leftX+10 > current_position.current_x+current_position.character_width:
                closest_right = i.leftX+10 
    return (closest_left, closest_right)



# In[6]:


class items:
    def __init__(self):
        self.milk = 0
        self.sugar = 0
        self.celery = 0
        self.butter = 0
        self.flour = 0
        self.vanilla = 0
        self.chocolate = 0
        
    def __str__(self):
        return "Milk:"+str(self.milk)+"\nSugar:"+str(self.sugar) 
        
    def total(self):
        return self.milk+self.sugar+self.celery+self.chocolate+self.vanilla+self.butter+self.flour
    
    def remove_random(self):
        #print("entered remove function")
        
        items_present = []
        if self.milk > 0:
            items_present.append(1)
        if self.sugar > 0:
            items_present.append(2)
        if self.celery > 0:
            items_present.append(3)
        if self.butter > 0:
            items_present.append(4)
        if self.flour > 0:
            items_present.append(5)
        if self.vanilla > 0:
            items_present.append(6)
        if self.chocolate > 0:
            items_present.append(7)
            
        if items_present:
            subtract = random.choice(items_present)
            if subtract == 1:
                self.milk -=1
            elif subtract == 2:
                self.sugar -=1
            elif subtract == 3:
                self.celery -=1
            elif subtract == 4:
                self.butter -=1
            elif subtract == 5:
                self.flour -=1
            elif subtract == 6:
                self.vanilla -=1
            elif subtract == 7:
                self.chocolate -=1
        else:
            pygame.mixer.Sound.play(lose_sound)
            global finish_line
            finish_line = True
            
            
class collision:
    def __init__(self, collision_type, stage):
        self.collision_type = collision_type
        self.stage = stage


def generate_ingredient_collisions(list_of_ingredients_on_screen, list_of_ingredients, current_position):
    ingredient_collisions = []
    current_position_rectangle = pygame.Rect(
        xy_position_to_pixels((current_position.current_x, current_position.current_y,
            current_position.character_width, current_position.character_height), virtual_window, window_size))
    for i in list_of_ingredients_on_screen:
        ingredient_rectange = pygame.Rect(xy_position_to_pixels(
            (i.ingredient_position_x, i.ingredient_position_y, i.size, i.size), 
            virtual_window, window_size))
        if current_position_rectangle.colliderect(ingredient_rectange):
            collision_temp = collision(i.ingredient_type, 0)
            ingredient_collisions.append(collision_temp)
            #print("added to ingredient collisions list")
            list_of_ingredients.remove(i)
    return ingredient_collisions


def process_collision_lists(position, list_of_ingredient_collisions, list_of_badbread_collisions, items):
    if list_of_ingredient_collisions:
        for i in list_of_ingredient_collisions:
            if i.stage == 0:
                if i.collision_type == "milk":
                    items.milk += 1
                elif i.collision_type == "sugar":
                    items.sugar += 1
                elif i.collision_type == "celery":
                    items.celery += 1
                elif i.collision_type == "butter":
                    items.butter += 1
                elif i.collision_type == "flour":
                    items.flour += 1
                elif i.collision_type == "vanilla":
                    items.vanilla += 1
                elif i.collision_type == "chocolate":
                    items.chocolate += 1
                i.stage += 1
                
    if list_of_badbread_collisions:
        for i in list_of_badbread_collisions:
            items.remove_random()
    


# In[7]:


def calculate_locations(left_bar, window_size, virtual_window):
    list_of_rectangles = []
    gap = float(virtual_window[1]-140)/8
    for i in range(7):
        rectangle = (left_bar,virtual_window[1]-((i+1)*gap + ((i+1)*20)), 20, 20)#IMAGE SIZE HARD CODED IN Y POSITON
        print(str(rectangle))
        pixel_rectangle = xy_position_to_pixels(rectangle, window_size, virtual_window)
        list_of_rectangles.append(pixel_rectangle)
    return list_of_rectangles

def blit_items(item_class, locations, font):
    if item_class.milk > 0:
        #print("bliting milk")
        screen.blit(milk_scaled,locations[0])
        textsurface = font.render("x"+str(item_class.milk), False, (255, 0, 193))
        xy_position_of_text = (locations[0][0]+130,locations[0][1]+20)
        screen.blit(textsurface,xy_position_of_text)  
    if item_class.chocolate > 0:
        screen.blit(chocolate_scaled,locations[1])
        textsurface = font.render("x"+str(item_class.chocolate), False, (255, 0, 193))
        xy_position_of_text = (locations[1][0]+130,locations[1][1]+20)
        screen.blit(textsurface,xy_position_of_text)
    if item_class.sugar > 0:
        screen.blit(sugar_scaled,locations[2])
        textsurface = font.render("x"+str(item_class.sugar), False, (255, 0, 193))
        xy_position_of_text = (locations[2][0]+130,locations[2][1]+20)
        screen.blit(textsurface,xy_position_of_text)
    if item_class.celery > 0:
        screen.blit(celery_scaled,locations[3])
        textsurface = font.render("x"+str(item_class.celery), False, (255, 0, 193))
        xy_position_of_text = (locations[3][0]+130,locations[3][1]+20)
        screen.blit(textsurface,xy_position_of_text)
    if item_class.butter > 0:
        screen.blit(butter_scaled,locations[4])
        textsurface = font.render("x"+str(item_class.butter), False, (255, 0, 193))
        xy_position_of_text = (locations[4][0]+130,locations[4][1]+20)
        screen.blit(textsurface,xy_position_of_text)
    if item_class.flour > 0:
        screen.blit(flour_scaled,locations[5])
        textsurface = font.render("x"+str(item_class.flour), False, (255, 0, 193))
        xy_position_of_text = (locations[5][0]+130,locations[5][1]+20)
        screen.blit(textsurface,xy_position_of_text)
    if item_class.vanilla > 0:
        screen.blit(vanilla_scaled,locations[6])
        textsurface = font.render("x"+str(item_class.vanilla), False, (255, 0, 193))
        xy_position_of_text = (locations[6][0]+130,locations[6][1]+20)
        screen.blit(textsurface, xy_position_of_text)


# In[8]:


class animation:
    def __init__(self, rectangles_left, rectangles_right, rectangle_forward):
        self.right = 0
        self.left = 0
        self.rectangles_left = rectangles_left
        self.rectangles_right = rectangles_right
        self.rectangle_forward = rectangle_forward
        
def create_character_rectangles(spritesheet_xy, direction):
    character_pixels = (spritesheet_xy[0]/4, spritesheet_xy[1]/8)
    rectangle_list = []
    if direction == "left":
        for i in range(4):
            rectangle_list.append((i*character_pixels[0], 0, character_pixels[0], character_pixels[1]))
        for i in range(4):
            rectangle_list.append((i*character_pixels[0], character_pixels[1], character_pixels[0], character_pixels[1]))
        return rectangle_list
    elif direction == "right":
        for i in range(4):
            rectangle_list.append((i*character_pixels[0],character_pixels[1]*4, character_pixels[0], character_pixels[1]))
        for i in range(4):
            rectangle_list.append((i*character_pixels[0], character_pixels[1]*5, character_pixels[0], character_pixels[1]))
        return rectangle_list
    elif direction == "forward":
        rectangle_list.append((0*character_pixels[0],character_pixels[1]*2, character_pixels[0], character_pixels[1]))
        return rectangle_list
def blit_character(current_position, window_size, virtual_window, animation_stage):
        character_position = xy_position_to_pixels(
        (current_position.current_x, current_position.current_y-2,current_position.character_width,current_position.character_height), window_size, virtual_window)
        if current_position.current_xs + current_position.wall_speed >  0:
            screen.blit(eggrika_spritesheet_scaled, character_position, animation_stage.rectangles_right[animation_stage.right])
            if animation_stage.right < 7:
                animation_stage.right += 1
            else:
                animation_stage.right = 0
        if current_position.current_xs + current_position.wall_speed  < 0:
            screen.blit(eggrika_spritesheet_scaled, character_position, animation_stage.rectangles_left[animation_stage.left])
            if animation_stage.left < 7:
                animation_stage.left += 1
            else:
                animation_stage.left = 0
        if current_position.current_xs + current_position.wall_speed == 0:
            screen.blit(eggrika_spritesheet_scaled, character_position, animation_stage.rectangle_forward[0])
            


# In[9]:


virtual_window = (300,200)
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.font.init()
pygame.mixer.init()
window_size = (pygame.display.Info().current_w -50, pygame.display.Info().current_h - 50)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Egg World")
global done
done = False
clock = pygame.time.Clock()

wall = None
block_generation_list = [(0,0,630,20),(390,110,20,40),(370,70,60,40),
                         (350,30,100,40),(330,0,140,30),(680,0,120,20),(800,0,180,60),(980,0,320,10),(1300,0,250,50),
                         (1300,100,300,50),
                         (1400,150,40,50), (1550,0,50,30),
                         (1600,0,200,10),(1830,0,30,130),(1910,0,30,160),(1990,0,30,170),(2070, 80, 100, 50),(2070,0,530,20),
                        (2500,0,120,70),(2620,0,380,20)]

list_of_blocks = generate_list_of_block_objects(block_generation_list)

platform_generation_list = [(150,200,100),(500,600,120),(1050,1100,120),(1100,1190,70),(1190,1240,120),(1700,1770,90),
                           (2830,2900,100)]

list_of_platforms = generate_list_of_platform_objects(platform_generation_list)

badbread_generation_list = [(150,20,280),(470,20,570),(800,60,900),(1600,10,1770),(2070,20,2400)]

list_of_badbreads = generate_list_of_badbreads(badbread_generation_list)

ingredient_generation_list = [("milk", 200, 130), ("celery", 250, 180), ("sugar", 340, 80), ("chocolate", 390, 160),
                              ("vanilla", 440, 80), ("butter", 550, 30), ("flour", 650, 100), ("milk", 770, 30),
                             ("celery", 830, 150),("butter", 860, 150),("milk", 890, 150), ("chocolate",1130,180),
                             ("butter",1130,80), ("milk", 1320, 160), ("milk", 1350, 160),("milk", 1380, 160), 
                              ("sugar", 1450, 70),("celery", 1560, 160), ("chocolate", 1720,30), ("sugar",1830,140),
                             ("sugar",1910,170),("sugar",1990,180), ("flour", 2290, 100), ("milk",2410,80)]

list_of_ingredients = generate_list_of_ingredients(ingredient_generation_list)
wall = None
world_speed = .5

in_title_screen = True
title_text = pygame.image.load('Title.png')
title_scaled = pygame.transform.scale(title_text, window_size)
title_block = block(0, 0, virtual_window[0],20)
scroll = 0
chase_animation = 0
chase_image1 = pygame.image.load('Chase1.png')
chase_rectangle = (2835, 108, 60, 60)
pixel_chase_rectangle = xy_position_to_pixels(chase_rectangle, window_size, virtual_window)
chase_pixel_size = (pixel_chase_rectangle[2], pixel_chase_rectangle[3])
chase_image1_transform = pygame.transform.scale(chase_image1, chase_pixel_size)
chase_image2 = pygame.image.load('Chase2.png')
chase_image2_transform = pygame.transform.scale(chase_image2, chase_pixel_size)
global finish_line
finish_line = False
start_over = False

itembar = items()

current_position = position(current_y= virtual_window[1], current_x = 20, wall_speed = world_speed)  
title_position = position(current_y= 20, wall_speed = 0, current_xs = 5)  

myfont = pygame.font.Font('Birdy Game.ttf', 30)
myfontlarge = pygame.font.Font('Birdy Game.ttf', 80)
gradient = pygame.image.load('Gradient.jpeg')
gradient_scaled = pygame.transform.scale(gradient, window_size)
texture = pygame.image.load('CakeTexture.jpeg')
texture_scaled = pygame.transform.scale(texture, window_size)

resize_material_rectangle = xy_position_to_pixels((0,0,20,20), window_size, virtual_window)
materials_size = (resize_material_rectangle[2], resize_material_rectangle[3])
butter_picture = pygame.image.load('Butter.png')
butter_scaled = pygame.transform.scale(butter_picture, materials_size)
milk_picture = pygame.image.load('Milk.png')
milk_scaled = pygame.transform.scale(milk_picture, materials_size)
vanilla_picture = pygame.image.load('Vanilla.png')
vanilla_scaled = pygame.transform.scale(vanilla_picture, materials_size)
celery_picture = pygame.image.load('Celery.png')
celery_scaled = pygame.transform.scale(celery_picture, materials_size)
chocolate_picture = pygame.image.load('Chocolate.png')
chocolate_scaled = pygame.transform.scale(chocolate_picture, materials_size)
sugar_picture = pygame.image.load('Sugar.png')
sugar_scaled = pygame.transform.scale(sugar_picture, materials_size)
flour_picture = pygame.image.load('Flour.png')
flour_scaled = pygame.transform.scale(flour_picture, materials_size)
resize_bread_rectangle = xy_position_to_pixels((0,0,45,45), window_size, virtual_window)
bread_size = (resize_bread_rectangle[2], resize_bread_rectangle[3])
bread_left = pygame.image.load('Bread_Left.png')
bread_left_scaled = pygame.transform.scale(bread_left, bread_size)
bread_right = pygame.image.load('Bread_Right.png')
bread_right_scaled = pygame.transform.scale(bread_right, bread_size)
custard_image = pygame.image.load('Custard.jpg')
custard_scaled = pygame.transform.scale(custard_image, window_size)
omelette_image = pygame.image.load('Omelette.jpg')
omelette_scaled = pygame.transform.scale(omelette_image, window_size)
quiche_image = pygame.image.load('Quiche.jpg')
quiche_scaled = pygame.transform.scale(quiche_image, window_size)
creme_image = pygame.image.load('CremeBrulee.jpg')
creme_scaled = pygame.transform.scale(custard_image, window_size)
pudding_image = pygame.image.load('Pudding.jpg')
pudding_scaled = pygame.transform.scale(pudding_image, window_size)
lose_image = pygame.image.load('Lose.jpg')
lose_scaled = pygame.transform.scale(lose_image, window_size)

left_bar = virtual_window[0]-50
spacing = 10
locations = calculate_locations(left_bar, window_size, virtual_window)

eggrika_spritesheet = pygame.image.load("EggrikaSpriteSheet.png")
spritesheet_size = xy_position_to_pixels((0,0,current_position.character_width*4, 
                                                     current_position.character_height*8), window_size, virtual_window)
spritesheet_xy = (spritesheet_size[2], spritesheet_size[3])
eggrika_spritesheet_scaled = pygame.transform.scale(eggrika_spritesheet, (spritesheet_size[2], spritesheet_size[3]))

rectangles_right = create_character_rectangles(spritesheet_xy, 'right')
rectangles_left = create_character_rectangles(spritesheet_xy, 'left')
rectangle_forward = create_character_rectangles(spritesheet_xy, 'forward')
animation_stage = animation(rectangles_left, rectangles_right, rectangle_forward)


jump_sound = pygame.mixer.Sound('Boing.ogg')
yay_bool = False
yay_sound = pygame.mixer.Sound('Yay.ogg')
theme_sound = pygame.mixer.Sound('Theme.ogg')
lose_sound = pygame.mixer.Sound('LoseAudio.ogg')
pygame.mixer.Sound.set_volume(theme_sound, .2)
pygame.mixer.Sound.set_volume(jump_sound, .1)
pygame.mixer.Sound.play(theme_sound, loops = -1)

while not done:
    
    while in_title_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    in_title_screen = False
        screen.blit(gradient_scaled,(0,0))
        blit_character(title_position, window_size, virtual_window, animation_stage)
        screen.blit(title_scaled,(0,0))
        blit_block(title_block, window_size, virtual_window, myfont)
        pygame.display.flip()
        if title_position.current_x < virtual_window[0]:
            title_position.current_x += title_position.current_xs
        if title_position.current_x >= virtual_window[0]:
            title_position.current_x = 0 - title_position.current_x - title_position.character_width
            
        #####
    
    if scroll <= 2730:
        scroll_everything_left(list_of_platforms, list_of_blocks, list_of_badbreads,list_of_ingredients, world_speed)
        chase_rectangle = (chase_rectangle[0]-world_speed,chase_rectangle[1], 50,50)
        scroll+=world_speed
    else:
        current_position.wall_speed = 0
    
    clock.tick(50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            #print("KEY DOWN!")
            current_position.button = keys(event)
            #print(current_position.button)
            break
        if event.type == pygame.KEYUP:
            #print("KEY UP!")
            current_position.button = None
            break
            
    blocks_on_screen = generate_list_of_blocks_on_screen(list_of_blocks, virtual_window)
    platforms_on_screen = generate_list_of_platforms_on_screen(list_of_platforms, virtual_window)
    wall = give_wall_value(current_position, blocks_on_screen)
    floor = give_floor_value(current_position, blocks_on_screen, platforms_on_screen)
    badbreads_on_screen = generate_list_of_badbreads_on_screen(list_of_badbreads, virtual_window)
    ingredients_on_screen = generate_list_of_ingredients_on_screen(list_of_ingredients, virtual_window)

    
    #Check If On-Screen
    if current_position.current_x < -150:
        itembar.remove_random()
    if current_position.current_y < -200:
        itembar.remove_random()
    
    
    #Collisions
    current_position.give_next_position(floor = floor, wall = wall)
    list_of_ingredient_collisions = generate_ingredient_collisions(ingredients_on_screen, list_of_ingredients, current_position)
    list_of_badbread_collisions = generate_badbread_collisions(badbreads_on_screen,
                                                               list_of_badbreads, current_position)
    
    process_collision_lists(current_position, list_of_ingredient_collisions, list_of_badbread_collisions, itembar)
    
    #Blit Sky
    screen.blit(gradient_scaled,(0,0))


    
    #Blit Structures/Enemies
    for i in blocks_on_screen:
        blit_block(i, window_size, virtual_window, myfont)
    for i in platforms_on_screen:
        blit_platform(i, window_size, virtual_window)
    for i in badbreads_on_screen:
        i.move_badbread()
        blit_badbread(i, window_size, virtual_window)
    for i in ingredients_on_screen:
        blit_ingredient(i, window_size, virtual_window)
    
    #Blit Items
    blit_items(itembar, locations, myfontlarge)
    
    #Chase:
    pixel_chase_rectangle = xy_position_to_pixels(chase_rectangle, window_size, virtual_window)
    if chase_animation < 30:
        screen.blit(chase_image1_transform, pixel_chase_rectangle)
        chase_animation+=1
    elif chase_animation < 60:
        screen.blit(chase_image2_transform, pixel_chase_rectangle)
        chase_animation+=1
    else:
        screen.blit(chase_image2_transform, pixel_chase_rectangle)
        chase_animation = 0
    
    #Test Stuff
    #current_position.current_x = 100
    #current_position.current_y = 150
    
    if current_position.current_x>chase_rectangle[0]:
        if yay_bool == False:
            pygame.mixer.Sound.play(yay_sound)
            yay_bool == True
        finish_line = True
    
    #Character
    blit_character(current_position, window_size, virtual_window, animation_stage)
    
    pygame.display.flip()
    
    
    while finish_line == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                print(itembar)
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    start_over = True
                    finish_line = False
        total = itembar.total()
        if total >= 23 and itembar.celery >= 3 and itembar.flour >=1:
            screen.blit(quiche_scaled, (0,0))
        elif total >=23 and itembar.celery >= 2:
            screen.blit(omelette_scaled, (0,0))
        elif total >= 20 and itembar.vanilla >= 1:
            screen.blit(omelette_scaled, (0,0))
        elif total >= 15 and itembar.chocolate >= 3:
            screen.blit(pudding_scaled, (0,0)) 
        elif total >= 5 and itembar.milk >= 1 and itembar.butter>=1 and itembar.flour >= 1:
            screen.blit(custard_scaled, (0,0))
        else:
            screen.blit(lose_scaled, (0,0))
            
        pygame.display.flip()
        
    if start_over == True:
        wall = None
        block_generation_list = [(0,0,630,20),(390,110,20,40),(370,70,60,40),
                                 (350,30,100,40),(330,0,140,30),(680,0,120,20),(800,0,180,60),(980,0,320,10),(1300,0,250,50),
                                 (1300,100,300,50),
                                 (1400,150,40,50), (1550,0,50,30),
                                 (1600,0,200,10),(1830,0,30,130),(1910,0,30,160),(1990,0,30,170),(2070, 80, 100, 50),(2070,0,530,20),
                                (2500,0,120,70),(2620,0,380,20)]

        list_of_blocks = generate_list_of_block_objects(block_generation_list)

        platform_generation_list = [(150,200,100),(500,600,120),(1050,1100,120),(1100,1190,70),(1190,1240,120),(1700,1770,90),
                                   (2830,2900,100)]

        list_of_platforms = generate_list_of_platform_objects(platform_generation_list)

        badbread_generation_list = [(150,20,280),(470,20,570),(800,60,900),(1600,10,1770),(2070,20,2400)]

        list_of_badbreads = generate_list_of_badbreads(badbread_generation_list)

        ingredient_generation_list = [("milk", 200, 130), ("celery", 250, 180), ("sugar", 340, 80), ("chocolate", 390, 160),
                                      ("vanilla", 440, 80), ("butter", 550, 30), ("flour", 650, 100), ("milk", 770, 30),
                                     ("celery", 830, 150),("butter", 860, 150),("milk", 890, 150), ("chocolate",1130,180),
                                     ("butter",1130,80), ("milk", 1320, 160), ("milk", 1350, 160),("milk", 1380, 160), 
                                      ("sugar", 1450, 70),("celery", 1560, 160), ("chocolate", 1720,30), ("sugar",1830,140),
                                     ("sugar",1910,170),("sugar",1990,180), ("flour", 2290, 100), ("milk",2410,80)]

        list_of_ingredients = generate_list_of_ingredients(ingredient_generation_list)
        wall = None
        in_title_screen = True
        scroll = 0
        itembar = items()
        chase_rectangle = (2835, 108, 60, 60)
        current_position = position(current_y= virtual_window[1], wall_speed = world_speed)  
        title_position = position(current_y= 20, current_x = 20, wall_speed = 0, current_xs = 5)  
        start_over = False
        
pygame.quit()


