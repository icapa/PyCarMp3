import pygame
from pygame.locals import *
import time
import datetime
import sys
import os
import glob
import subprocess

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/event0"
os.environ["SDL_MOUSEDRV"] = "TSLIB"


#screen size
width  = 320
height = 240
size = (width, height)
screen = pygame.display.set_mode(size)


pygame.init()

#disable mouse cursor
pygame.mouse.set_visible(False)


skin1 = pygame.image.load("PyCarMp3.png")

print skin1

screen.blit(skin1, (0, 0))

pygame.display.update()
while True:
	time.sleep(2)
