import time
import random
import pygame
import pygame.midi
import numpy as np
from typing import Tuple

__author__ = "Thomas Heller"

AV_SIZE  = 20
WIN_X    = 30 * AV_SIZE
WIN_Y    = 30 * AV_SIZE
DIFF_MAX = np.sqrt(WIN_X**2 + WIN_Y**2)

def adapt_avatar_position(event, user_x_pos:int, user_y_pos:int) -> Tuple[int, int]:
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            if user_x_pos >= AV_SIZE:
                user_x_pos -= AV_SIZE
        if event.key == pygame.K_RIGHT:
            if user_x_pos < WIN_X-AV_SIZE:
                user_x_pos += AV_SIZE
        if event.key == pygame.K_UP:
            if user_y_pos >= AV_SIZE:
                user_y_pos -= AV_SIZE
        if event.key == pygame.K_DOWN:
            if user_y_pos < WIN_Y-AV_SIZE:
                user_y_pos += AV_SIZE
    return user_x_pos, user_y_pos

def calculate_difference(win_position:tuple, user_x_pos:int, user_y_pos:int):
    difference = abs(win_position[0] - user_x_pos), abs(win_position[1] - user_y_pos)
    return np.sqrt(np.sqrt(difference[0]**2 + difference[1]**2) / DIFF_MAX)

def main():

    # setup
    pygame.init()

    pygame.midi.init()
    player = pygame.midi.Output(0)
    player.set_instrument(0)
    current_note = random.randint(60,84)
    
    window = pygame.display.set_mode((WIN_X,WIN_Y))

    user_x_pos, user_y_pos = int(WIN_X/2), int(WIN_Y/2)

    pos_x = [ii for ii in range(0,WIN_X-AV_SIZE,AV_SIZE)]
    pos_y = [ii for ii in range(0,WIN_Y-AV_SIZE,AV_SIZE)]
    win_position = (random.choice(pos_x), random.choice(pos_y))

    difference = calculate_difference(win_position, user_x_pos, user_y_pos)
    player.note_on(current_note, int(127*(1-difference)))
    
    old_time = time.time()

    # program loop
    running = True
    while running:
        if win_position == (user_x_pos, user_y_pos):
            window.fill((255,255,0))
        else:
            window.fill((255,255,255))

        difference = calculate_difference(win_position, user_x_pos, user_y_pos)

        pygame.draw.rect(window,(0,50,255,50),(user_x_pos,user_y_pos,AV_SIZE,AV_SIZE))  # Rect(left, top, width, height) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            user_x_pos, user_y_pos = adapt_avatar_position(event, user_x_pos, user_y_pos)
        pygame.display.flip()  # Documentation: Update the full display Surface to the screen

        if time.time()-old_time > 1:
            player.note_off(current_note)
            current_note = random.randint(60,84)
            player.note_on(current_note, int(127*(1-difference)))
            old_time = time.time()
    
    # teardown
    del player
    pygame.midi.quit()
     
if __name__=="__main__":
    main()