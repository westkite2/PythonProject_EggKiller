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
import constants
from spritesheet_functions import SpriteSheet
 
class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """    

    # -- Methods    
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # -- Attributes
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # The direction that the player is facing
        self.direction = "R"

        path = os.path.join(os.path.dirname(__file__), "assets/spritesheet_player.png")
        sprite_sheet = SpriteSheet(path)

        # load right facing image into a list
        image = sprite_sheet.get_image(0, 0, 60, 90)
        self.walking_r = image

        # Load and flip the right facing image to face left.
        image = sprite_sheet.get_image(0, 0, 60, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_l = image

        # Load down facing image into a list
        image = sprite_sheet.get_image(60, 0, 60, 90)
        self.walking_d = image

        # Load up facing image into a list
        image = sprite_sheet.get_image(120, 0, 60, 90)
        self.walking_u = image
 
        # Set the image the player starts with
        self.image = self.walking_r
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the player. """
 
        # Update position
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Update player image
        pos = self.rect.x
        if self.direction == "R":
            self.image = self.walking_r
        elif self.direction == "L":
            self.image = self.walking_l
        elif self.direction == "U":
            self.image = self.walking_u
        elif self.direction == "D":
            self.image = self.walking_d
        
    # Player movement
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 5
        self.direction = "R"
        
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -5
        self.direction = "L"
    
    def go_up(self):
        """ Called when the user hits the right arrow. """
        self.change_y = -5
        self.direction = "U"
    
    def go_down(self):
        """ Called when the user hits the right arrow. """
        self.change_y = 5
        self.direction = "D"
    
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
        self.change_y = 0


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.direction = "R"

        self.image = pygame.Surface([5, 5])
        self.image.fill(constants.BLUE)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        if self.direction == "R":
            self.rect.x += 12
        elif self.direction == "L":
            self.rect.x -= 12
        elif self.direction == "U":
            self.rect.y -= 12
        elif self.direction == "D":
            self.rect.y += 12