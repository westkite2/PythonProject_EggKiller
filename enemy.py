# 장서연 20191144
# Introduction to Visual Media Programming
# Date: 21.11.26
# TOPIC: Shooting game

"""
This is used to hold the Player class.
The Player represents the user-controlled sprite on the screen.
"""
import os
import pygame
import random
import time
import constants
from spritesheet_functions import SpriteSheet

class Egg(pygame.sprite.Sprite):
    """ This class represents the Egg. """

    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # -- Attributes
        # flag variables
        self.dead_flag = 0
        self.grown_flag = 0

        # Holds all the images for the animated egg
        self.growing_egg = []

        path = os.path.join(os.path.dirname(__file__), "assets/spritesheet_egg.png") 
        sprite_sheet = SpriteSheet(path)
        # Load all the egg images into a list
        image = sprite_sheet.get_image(0, 0, 50, 36)
        self.growing_egg.append(image)
        image = sprite_sheet.get_image(50, 0, 50, 36)
        self.growing_egg.append(image)
        image = sprite_sheet.get_image(100, 0, 50, 36)
        self.growing_egg.append(image)
        image = sprite_sheet.get_image(150, 0, 50, 36)
        self.growing_egg.append(image)
        image = sprite_sheet.get_image(200, 0, 50, 36)
        self.growing_egg.append(image)
        
        self.broken_egg = sprite_sheet.get_image(250, 0, 50, 36)

        # Set the image the egg starts with
        self.image = self.growing_egg[0]
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        self.start = time.time()


    def update(self):
        """ Change egg status """
        if self.dead_flag == 0:
            # if egg is alive, then grow
            grown_time = int(time.time() - self.start)
            frame = (grown_time // 2) % len(self.growing_egg)
            self.image = self.growing_egg[frame]
            if frame == (len(self.growing_egg) - 1): #if fully grown
                self.grown_flag = 1      
        elif self.dead_flag == 1:
            # if the egg is dead, then crack
            self.image = self.broken_egg


class Bug(pygame.sprite.Sprite):
    """ This class represents the Bug. """

    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # -- Attributes
        # dead bug
        self.dead_flag = 0

        # Set speed vector of the bug
        self.change_x = 0
        self.change_y = 0

        # Choose direction to move
        self.direction_list = ["R", "L", "U", "D"]
        self.direction = self.direction_list[random.randrange(0, 4)]

        path = os.path.join(os.path.dirname(__file__), "assets/spritesheet_bug.png") 
        sprite_sheet = SpriteSheet(path)
        # Load all the egg images into a list
        image = sprite_sheet.get_image(0, 0, 80, 75)
        self.bug_d = image
        self.bug_u = pygame.transform.rotate(image, 180)

        image = sprite_sheet.get_image(80, 0, 80, 75)
        self.bug_r = image
        self.bug_l = pygame.transform.flip(image, True, False)

        self.broken_bug = sprite_sheet.get_image(160, 0, 80, 75)

        # Set the image the egg starts with
        self.image = self.bug_d
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        self.start = time.time()

    def update(self):
        """ Bug mechanism """
        # If the bug is dead, then change image
        if self.dead_flag == 1:
            self.image = self.broken_bug
        else:
            # Bug Border check
            if self.rect.x < 0:
                self.rect.x = 0
                self.direction = self.direction_list[random.randrange(0, 4)] 
            elif self.rect.right >= constants.SCREEN_WIDTH:
                self.rect.right = constants.SCREEN_WIDTH
                self.direction = self.direction_list[random.randrange(0, 4)] 
            elif self.rect.y < 0:
                self.rect.y = 0
                self.direction = self.direction_list[random.randrange(0, 4)] 
            elif self.rect.bottom > constants.SCREEN_HEIGHT:
                self.rect.bottom = constants.SCREEN_HEIGHT
                self.direction = self.direction_list[random.randrange(0, 4)] 

            # Update position
            self.move()
                

    def move(self):
        if self.direction == "R":
            self.change_x = 3
            self.change_y = 0
            self.image = self.bug_r
        elif self.direction == "L":
            self.change_x = -3
            self.change_y = 0
            self.image = self.bug_l
        elif self.direction == "U":
            self.change_y = -3
            self.chang_x = 0
            self.image = self.bug_u
        elif self.direction == "D":
            self.change_y = 3
            self.change_x = 0
            self.image = self.bug_d

        self.rect.x += self.change_x
        self.rect.y += self.change_y
    