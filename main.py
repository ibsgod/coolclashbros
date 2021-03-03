import pygame
import os
import sys

import Info
from Fisty import Fisty
from Ground import Ground
from Swordy import Swordy

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
width = 1300
height = 650
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
Info.grounds.append(Ground((width - 900) / 2, height - 200, 900, 100, screen))
Info.heroes.append(Fisty((width-100)/2, 400, screen, True))
Info.heroes.append(Swordy((width+100)/2, 400, screen, True))
for i in Info.heroes:
    Info.hpText[i] = pygame.font.SysFont("Microsoft Yahei UI Light", 35).render("0%", True, (0, 0, 0))

while True:
    screen.fill((255, 255, 255))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
    for i in Info.heroes:
        i.tick(events)
    for i in Info.grounds:
        i.draw()
    textx = 100
    for i in Info.heroes:
        i.draw()
        screen.blit(Info.hpText[i],(textx, 50))
        textx += 100

    pygame.display.update()
    clock.tick(60)