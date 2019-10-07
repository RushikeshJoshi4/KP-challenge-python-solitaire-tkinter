import pygame
import sys
import time
pygame.init()
screen = pygame.display.set_mode((1000,100))

while True:
    for event in pygame.event.get():
        print("time: "+str(time.time()))