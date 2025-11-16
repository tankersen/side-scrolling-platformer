# tutorial being used: https://www.youtube.com/watch?v=6gLeplbqtqg
# i am first going through to follow the tutorial, then will be making changes once i create the base code
# i will outline the core changes i make as i go in the pseudo code
# asset folder currently has placeholders, i will be making different art

import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer")

bg_color = (255,255,255)
x, y = 1920, 1080
fps = 60
player_velocity = 5

window = pygame.display.set_mode((x,y))

def get_background(name):
    image = pygame.image.load(join("assets","Background",name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(x // width + 1):
        for j in range(y // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

def draw(window,background, bg_image):
    for tile in background:
        window.blit(bg_image, tile)

    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

#regulate framerate across devices
    run = True
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window, background, bg_image)

if __name__ == "__main__":
    main(window)