__author__ = 'andy.cheung'

import pygame
#from math import hypot
import math
import random
import copy
import itertools
import time

from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys

#GLOBAL VARIABLES
screen_x = 500
screen_y = 500
screen = None
font = None
city_color = [10, 10, 200]  # blue
city_radius = 3
font_color = [255, 255, 255]  # white
cities = []
keys = []
genrationLimit = 50


def fromFile(file):
    #Load cities from file
    f = open(file, 'r')
    cities.clear()
    for line in f:
        comp = line.rstrip('\n').split(' ')
        city = ((int(comp[1]), int(comp[2])))
        keys.append(comp[0])
        cities.append(city)

    return cities


def loadGUI():
    global screen, font
    pygame.init()
    pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Travelling salesman problem')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)


def byText():
    global screen, gui
    gui = True

    if screen is None:
        gui = False
        loadGUI()

    collecting = True
    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
                drawLines()
            draw_cities(cities)


def byMouse():
    global screen, gui
    gui = True

    if screen is None:
        gui = False
        loadGUI()

    collecting = True
    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
                drawLines()
            elif event.type == MOUSEBUTTONDOWN:
                cities.append(pygame.mouse.get_pos())
                draw_cities(cities)


def drawLines():
    screen.fill(0)
    #screen.fill(0)
    pygame.draw.lines(screen, city_color, True, cities)
    text = font.render("Un chemin, pas le meilleur!", True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN: break


def draw_cities(positions, connected=False, generation=-1, distance=-1):
    """Draw the cities passed in argument to the GUI"""
    # GUI mode selected

    global screen, city_radius, font_color
    if screen is not None:
        screen.fill(0)
        for pos in range(0, len(positions)):
            pygame.draw.circle(screen, city_color, positions[pos], city_radius)
            myCityName = font.render("City %i : [%i %i]" % (pos, positions[pos][0], positions[pos][1]), True,
                                     font_color)
            cityNameRec = positions[pos]
            screen.blit(myCityName, cityNameRec)
        if connected:
            pygame.draw.lines(screen, city_color, True, positions)

        if generation != -1 and distance != -1:
            text = font.render('Generation n°' + str(generation) + '; Distance = ' + str(round(distance, 2)), True,
                                    font_color, (0, 0, 0))
            textrect = text.get_rect()
            textrect.centerx = screen_x / 2.0
            textrect.centery = screen_y - 20 / 4.0
            screen.blit(text, textrect)
        pygame.display.flip()

def distanceTotal(solution):
    distanceTot = 0
    cityB = None
    for city in solution:
        cityA = cityB
        cityB = city
        if cityA is not None and cityB is not None:
            distanceTot += distance_euclidian(cityA, cityB)
    distanceTot += distance_euclidian(solution[0], solution[len(solution) - 1])

    return distanceTot

def distance_euclidian(cityA, cityB):
    return math.sqrt((cityA[0] - cityB[0]) * (cityA[0] - cityB[0]) +
                     (cityA[1] - cityB[1]) * (cityA[1] - cityB[1]))

def createPopulation(cities):
    population = []
    while len(population) < len(cities):
        solution = cities.copy()
        random.shuffle(solution)
        solution = [solution, distanceTotal(solution)]
        population.append(solution)
    return population

def ga_solve(file=None, gui=True, maxtime=0):

    global cities, keys
    t = time.time()

    try:
        file = sys.argv[1]

    except IndexError:
        # aucun arguement
        print("Sans fichier")

    if gui:
        loadGUI()

    if file is not None:
        cities = fromFile(file)
        #byText()
    else:
        byMouse()
    draw_cities(cities)

    population = createPopulation(cities)
    print(population)
    generationNotOptimal = 0
    fitness = None
    generation = 0

    while (maxtime == 0 and generationNotOptimal < genrationLimit) or t < maxtime:
        population.sort(key=lambda s: s[1])
        if fitness is None or fitness[1] > population[0][1]:
            generationNotOptimal = 0
            fitness = [population[0][0].copy(), population[0][1]]
            print(fitness)

        draw_cities(fitness[0], True, generation, fitness[1])



        elites = selection(population)
        #print(elites)

        children = crossover(elites)

        population = elites + children
        for i in range(0, int(len(population)* 0.2)):
            mutate(population[random.randint(0, len(population)-1)][0])

        generation += 1
        generationNotOptimal += 1
    print(distanceTotal(fitness[0]), [c[0] for c in fitness[0]])

def mutate(solution):
    p1 = random.randint(0, len(solution) - 1)
    p2 = p1
    while p1 == p2:
        p2 = random.randint(0, len(solution) - 1)
    if p1 > p2:
        p1, p2 = p2, p1

    while p1 < p2:

        solution[p1], solution[p2] = solution[p2], solution[p1]
        p1 += 1
        p2 -= 1

def crossover(chromosomes):
    future_solution = []
    for i in range(0, int(round(0.3/2))):
        solution1 = chromosomes
        solution2 = chromosomes
        while solution2 == solution1:
            solution2 = chromosomes

        future_solution.append(crossoverVamos(solution1, solution2))
        future_solution.append(crossoverVamos(solution2, solution1))
    return future_solution

def crossoverVamos(ga, gb):
    fa, fb = True, True
    n = len(ga)
    town = ga
    x = ga.index(town)
    y = gb.index(town)
    g = [town]

    while fa or fb:
        x = (x - 1) % n
        y = (y + 1) % n
        if fa:
            if ga[x] not in g:
                g.insert(0, ga[x])
            else:
                fa = False
        if fb:
            if gb[y] not in g:
                g.append(gb[y])
            else:
                fb = False

    remaining_towns = []
    if len(g) < len(ga):
        while len(g)+len(remaining_towns) != n:
            x = (x - 1) % n
            if ga[x] not in g:
                remaining_towns.append(ga[x])
        random.shuffle(remaining_towns)  # Use Fisher-Yates shuffle, O(n). Better than copying and removing
        while len(remaining_towns) > 0:
            g.append(remaining_towns.pop())

    return g
#Elitisme
def selection(population):
    return [population[i] for i in range(0, int(len(cities) * 0.3))]




if __name__ == "__main__":
    import sys, os, getopt
    #Example from the python documentation
    opts = []
    try:
        opts = getopt.getopt(
            sys.argv[1:],
            "hnm:v",
            ["help", "no-gui", "maxtime=", "verbose"])[0]
    except getopt.GetoptError:
        print("Wrong options or params.")
        exit(2)

    gui = True
    verbose = False
    max_time = 0

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            exit()
        elif opt in ("-n", "--no-gui"):
            gui = False
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-m", "--maxtime"):
            max_time = int(arg)

    filename = None
    if len(sys.argv) > 1 and os.path.exists(sys.argv[-1]):
        filename = sys.argv[-1]
    ga_solve(filename, gui, max_time)
