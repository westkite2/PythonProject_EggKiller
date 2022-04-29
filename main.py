# 장서연 20191144
# Introduction to Visual Media Programming
# Date: 21.11.26
# TOPIC: Shooting game

import os
import pygame
import random
import constants
import background
from player import Player
from player import Bullet
from enemy import Egg, Bug

def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("The Egg Killer - created by 장서연")


    # load the sounds
    path = os.path.join(os.path.dirname(__file__), "assets/shoot.mp3")
    shoot_au = pygame.mixer.Sound(path)
    path = os.path.join(os.path.dirname(__file__), "assets/boom.mp3")
    boom_au = pygame.mixer.Sound(path)

    # --- Sprite lists
    active_sprite_list = pygame.sprite.Group()
    egg_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    bug_list = pygame.sprite.Group()

    # --- Create the sprites
    # Create the egg
    for i in range(10):
        egg = Egg()
    
        # Set a random location for the egg
        egg.rect.x = random.randrange(0, constants.SCREEN_WIDTH-50)
        egg.rect.y = random.randrange(0, constants.SCREEN_HEIGHT-50)
    
        # Add to the list of objects
        egg_list.add(egg)
        active_sprite_list.add(egg)

    # Create the player
    player = Player()
    player.rect.x = constants.SCREEN_WIDTH/2
    player.rect.y = constants.SCREEN_HEIGHT/2
    active_sprite_list.add(player)

    score = 0
    gameover_flag = 0 # not started the game yey

    #Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag to exit this loop

            # Restart
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameover_flag == 1 or gameover_flag == 2:
                    done = True
                    

            # Player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.go_up()
                if event.key == pygame.K_DOWN:
                    player.go_down()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_UP and player.change_y < 0:
                    player.stop()
                if event.key == pygame.K_DOWN and player.change_y > 0:
                    player.stop()

            # Bullet shooting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Fire a bullet if the user clicks the mouse button
                    bullet = Bullet()
                    shoot_au.play()
                    # Set the bullet so it is where the player is
                    if player.direction == "R":
                        bullet.rect.x = player.rect.x + 50
                        bullet.rect.y = player.rect.y + 35
                        bullet.direction = player.direction
                    elif player.direction == "L":
                        bullet.rect.x = player.rect.x + 10
                        bullet.rect.y = player.rect.y + 35
                        bullet.direction = player.direction
                    elif player.direction == "U":
                        bullet.rect.x = player.rect.x + 30
                        bullet.rect.y = player.rect.y + 5
                        bullet.direction = player.direction
                    elif player.direction == "D":
                        bullet.rect.x = player.rect.x + 31
                        bullet.rect.y = player.rect.y + 60
                        bullet.direction = player.direction                                                
                    # Add the bullet to the lists
                    active_sprite_list.add(bullet)
                    bullet_list.add(bullet)
                    

        # --- Game logic

        # Update all the sprites
        active_sprite_list.update()


        # Game Success if all enemies are killed
        while(True):
            cnt = 0
            for egg in egg_list:
                if(egg.dead_flag == 1):
                    cnt += 1
            for bug in bug_list:
                if(bug.dead_flag == 1):
                    cnt += 1
            if cnt == len(egg_list) + len(bug_list):
                gameover_flag = 2 # success
                break
            else:
                break
        
        # Player Border check
        if player.rect.x < 0:
            player.rect.x = 0
        if player.rect.right >= constants.SCREEN_WIDTH:
            player.rect.right = constants.SCREEN_WIDTH
        if player.rect.y < 0:
            player.rect.y = 0
        if player.rect.bottom > constants.SCREEN_HEIGHT:
            player.rect.bottom = constants.SCREEN_HEIGHT

        # See if the player bumps into the egg
        egg_bump_list = pygame.sprite.spritecollide(player, egg_list, False)
        for egg in egg_bump_list:
            if egg.dead_flag == 0:
                # If moving right, set right side to the left side of the item we hit
                if player.change_x > 0:
                    player.rect.right = egg.rect.left
                # If moving left, do the opposite.
                elif player.change_x < 0:
                    player.rect.left = egg.rect.right
                # If moving up, set top side to the bottom side of the item we hit
                elif player.change_y < 0:
                    player.rect.top = egg.rect.bottom
                # If moving left, do the opposite.
                elif player.change_x < 0:
                    player.rect.bottom = egg.rect.top
        
        # Gameover if the player bumps into the bug
        bug_bump_list = pygame.sprite.spritecollide(player, bug_list, False)
        for bug in bug_bump_list:
            if bug.dead_flag == 0:
                gameover_flag = 1

        # Calculate mechanics for each bullet
        for bullet in bullet_list:
            # See if it hits an egg
            egg_hit_list = pygame.sprite.spritecollide(bullet, egg_list, False)
    
            # For each hit, remove the bullet and add to the score
            for egg in egg_hit_list:
                if egg.dead_flag == 0:
                    egg.dead_flag = 1
                    bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)
                    score += 10
                    boom_au.play()
            
            # See if it hits a bug
            bug_hit_list = pygame.sprite.spritecollide(bullet, bug_list, False)
            
            # For each hit, remove the bullet and add to the score
            for bug in bug_hit_list:
                if bug.dead_flag == 0:
                    bug.dead_flag = 1
                    bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)
                    score += 50
                    boom_au.play()

            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)

        # Egg Hatches
        for egg in egg_list:
            if egg.grown_flag == 1:
                # Create bug
                bug = Bug()
                active_sprite_list.add(bug)
                bug_list.add(bug)
                bug.rect.x = egg.rect.x
                bug.rect.y = egg.rect.y
                # Remove egg
                egg.dead_flag = 1
                egg.image = bug.broken_bug
                egg_list.remove(egg)
                active_sprite_list.remove(egg)


        # --- Draw a frame
        # clear the screen
        screen.fill(constants.WHITE)
        
        #draw background
        background.Draw(screen)

        if gameover_flag == 1:
            font = pygame.font.SysFont("Calibri", 25, True, False)
            text = font.render("Game Over!", True, constants.BLACK)
            center_x = (constants.SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (constants.SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        elif gameover_flag == 2: # success
            font = pygame.font.SysFont("Calibri", 25, True, False)
            text = font.render("Game Clear!", True, constants.BLACK)
            center_x = (constants.SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (constants.SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])   
            

        else:
            # draw active sprites
            active_sprite_list.draw(screen)
            
            # display the score
            # font, size, bold, italics
            font = pygame.font.SysFont('Calibri', 25, True, False)
            # Render the text. "True" means anti-aliased text.
            text = font.render(str(score), True, (255, 0, 0))
            # Put the image of the text on the screen at 250x250
            screen.blit(text, [constants.SCREEN_WIDTH/2, 20])

        # --- Limit frames per second
        clock.tick(constants.FPS)
 
        # Update the screen with what is drawn.
        pygame.display.flip()
 
    pygame.quit()
 
if __name__ == "__main__":
    main()