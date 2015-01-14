__author__ = 'andy.cheung'

import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys

screen_x = 500
screen_y = 500

city_color = [10,10,200] # blue
city_radius = 3

font_color = [255,255,255] # white

pygame.init()
window = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption('Fernandes Cheung : Travelling salesman problem')
screen = pygame.display.get_surface()
font = pygame.font.Font(None,30)

def draw(positions):
    screen.fill(0)

    for pos in range(0, len(positions)):
        pygame.draw.circle(screen,city_color,positions[pos],city_radius)
        myCityName = font.render("City %i : [%i %i]" %(pos, positions[pos][0], positions[pos][1]), True, font_color)
        cityNameRec = positions[pos]
        screen.blit(myCityName,cityNameRec)

    text = font.render("Nombre: %i" % len(positions), True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


listCities = []
count = 0

cities = []
draw(cities)

collecting = True

while collecting:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN and event.key == K_RETURN:
            collecting = False
        elif event.type == MOUSEBUTTONDOWN:
            cities.append(pygame.mouse.get_pos())
            draw(cities)


screen.fill(0)
pygame.draw.lines(screen,city_color,True,cities)
text = font.render("Un chemin, pas le meilleur!", True, font_color)
textRect = text.get_rect()
screen.blit(text, textRect)
pygame.display.flip()

while True:
	event = pygame.event.wait()
	if event.type == KEYDOWN: break

class Ville():
    def __init__(self, nom, x, y):
        self._nom = nom
        self._x = x
        self._y = y


def ga_solve(file = None, gui = True, maxtime = 0):
    return