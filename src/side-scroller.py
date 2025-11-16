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

pygame.display.setcaption("Platformer")

bg_color = (255,255,255)
width, height = 1920, 1080
fps = 60
player_velocity = 5

window = pygame.display.set_mode((width,height))

def main(window):
    clock = pygame.time.Clock()

if __name__ == "__main__":
    main(window)