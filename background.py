# 장서연 20191144
# Introduction to Visual Media Programming
# Date: 21.11.26
# TOPIC: Shooting game

import pygame
import os
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

def Draw(screen):
    path = os.path.join(os.path.dirname(__file__), "assets/tile.png")
    image = pygame.image.load(path).convert()

    # Positions of the tile
    tile_pos_list = []

    for i in range(0, SCREEN_WIDTH//100 + 1):
        for j in range(0, SCREEN_HEIGHT//100 + 1):
            if i == 0:
                x = 0
            else:
                x = i * 100
            if j == 0:
                y = 0
            else:
                y = j * 100
            tile_pos_list.append([x, y])
    for each in tile_pos_list:
        # Copy image to screen
        screen.blit(image, each)