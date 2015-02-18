__author__ = 'andy.cheung'

import pygame
#from math import hypot
import math
import random
import copy

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


def fromFile(file):
    #Load cities from file
    f = open(file, 'r')
    cities.clear()
    for line in f:
        comp = line.rstrip('\n').split(' ')
        city = ((int(comp[1]), int(comp[2])))
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
    #screen.fill(0)
    pygame.draw.lines(screen, city_color, True, cities)
    text = font.render("Un chemin, pas le meilleur!", True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN: break


def draw_cities(positions):
    """Draw the cities passed in argument to the GUI"""
    # GUI mode selected

    global screen, city_radius, font_color
    if screen is not None:
        screen.fill(0)
        for pos in range(0, len(positions)):
            print(positions[pos])
            pygame.draw.circle(screen, city_color, positions[pos], city_radius)
            myCityName = font.render("City %i : [%i %i]" % (pos, positions[pos][0], positions[pos][1]), True,
                                     font_color)
            cityNameRec = positions[pos]
            screen.blit(myCityName, cityNameRec)

        pygame.display.flip()


class Ville():
    def __init__(self, nom, x, y):
        self._nom = nom
        self._x = x
        self._y = y

# individu reprsentant une solution
class Individu():
    def __init__(self, id, cities):
        # table des villes + shuffle qui ne marche pas
        self._chromosome = sorted(cities, key=lambda k: random.random())
        self._id = id
        self._distance = 0
        self.calculateDistance()

    @staticmethod
    def distanceEuclidian(cityA, cityB):
        return math.hypot(cityB._x - cityA._x, cityB._y - cityA._y)


    def calculateDistance(self):
        for k in range(len(self._chromosome) - 1):
            self._distance += self.distanceEuclidian(self._chromosome[k], self._chromosome[k + 1])

        return self._distance

    def mutation(self):
        j = i = random.randint(0, len(self._chromosome) - 1)

        # pour éviter deux valeurs identiques
        while j == i:
            j = random.randint(0, len(self._chromosome) - 1)

        if i > j:
            i, j = j, i

        while i < j:
            self._chromosome[i], self._chromosome[j] = self._chromosome[j], self._chromosome[i]
            i += 1
            j -= 1


class Population():
    NB_POPULATION = 1
    CRITERIA_EVAL = 1
    SELECTED = 0.3

    def __init__(self, cities):

        self._cities = cities
        self.NB_POPULATION = len(cities)
        self._bestSolution = None
        self._maxima = float("inf")

        # population de solutions
        self._population = []

        # 2nd pass de solution
        self._nextPopulation = []

        # permet de creer une population de solutions
        for l in range(0, self.NB_POPULATION):
            self._population.append(Individu(l, self._cities))

    # methode de selection
    def selection(self, population):

        #global NB_POPULATION

        selected = []
        copyPop = copy.deepcopy(population)

        copyPop.sort(key=lambda x: x._distance)

        for i in copyPop._population:
            print(copyPop._population._distance)

        for p in range(int(self.NB_POPULATION * self.SELECTED)):
            selected = copyPop[p]

        return selected

        # methode de selection
        # def selection(self):
        #
        #     #global NB_POPULATION
        #
        #     selected = []
        #     copyPop = copy.deepcopy(self._population)
        #
        #     print(self._population)
        #     print("cpy")
        #     print(copyPop)
        #
        #     copyPop.sort(key=lambda x: x._distance, reverse=False)
        #
        #     for i in copyPop._population:
        #         print(copyPop._population._distance)
        #
        #     for p in range(int(self.NB_POPULATION * self.SELECTED)):
        #         selected = copyPop[p]
        #
        #     return selected

        # for k in range(len(self._population)):
        #     self._tabEntier.append(k)
        #
        # for sol in self._population :
        #     distance = sol._distance
        #
        #     if max < distance:
        #         max = distance
        #
        # for k in range(len(self._population)):
        #     if self._population[k].calculateDistance() < max:
        #         del self._population[k]

    def greedy_crossover(self, chromosomeA, chromosomeB):

        fa, fb = True
        n = len(chromosomeA)

        town = random.choice(chromosomeA)

        x = chromosomeA.index(town)
        y = chromosomeB.index(town)

        offspring = [town]

        while fa == True or fb == True:

            x = (x - 1) % n
            y = (y + 1) % n

            if fa:
                if chromosomeA[x] != offspring:
                    offspring.insert(0, chromosomeA[x])
                else:
                    fa = False

            if fb:
                if chromosomeB[y] != offspring:
                    offspring.append(chromosomeB[y])
                else:
                    fb = False

        rest = []

        if len(offspring) < len(chromosomeA):
            while len(offspring) + len(rest) != n :
                x = (x - 1) % n
                if chromosomeA[x] != offspring:
                    rest.append(chromosomeA[x])
                random.shuffle(rest)

            while len(rest) > 0 :
                offspring.append(rest.pop())
            
        return Population(offspring)

    def show(self):
        for i in range(len(self._population)):
            print(self._population[i]._id)
            print(self._population[i]._chromosome)


def ga_solve(file=None, gui=True, maxtime=0):

    global cities

    print("ga_solve")

    myCities = []

    for i in range(len(cities)):
        myCities.append(Ville(i,cities[i]))

    ind = Individu(1, myCities)

    population = Population(ind)
    generate = 0

    generate_limite = 1000

    while generate < generate_limite:
        for i in range(len(population._population)):
            population._population[i].mutate()
        generate += 1
        draw_cities(population._population)


if __name__ == "__main__":
    # nom, x, y):

    gui = True
    file = None
    try:
        file = sys.argv[1]

    except IndexError:
        # aucun arguement
        print("Sans fichier")
    #     draw_scene()
    #     sys.exit(1)

    if gui:
        loadGUI()

    if file is not None:
        cities = fromFile(file)
        byText()

    else:
        byMouse()

    draw_cities(cities)

    print(cities)

    ga_solve(file,gui,0)


    # a = Ville("a", 5, 10)
    # b = Ville("b", 1, 10)
    # c = Ville("c", 5, 17)
    # d = Ville("d", 9, 1)
    # e = Ville("e", 5, 10)
    # f = Ville("f", 1, 10)
    # g = Ville("g", 5, 17)
    # h = Ville("h", 9, 1)
    #
    # cities = [a, b, c, d, e, f, g, h]
    #
    # ind = Individu(1, cities)
    #
    # print(ind._chromosome)
    #
    # val = ind.calculateDistance()
    #
    # print(val)
    #
    # pop = Population(cities)
    #
    # print(val)

    # try:
    #     # partie avec fichier externe / ex : 10 pb005.txt
    #     filename = sys.argv[2]
    #     nb = int(sys.argv[1])
    #
    #     f = open(filename, "r")
    #     lines = f.readlines()
    #
    #     print("Avec fichier")
    #
    #     for i in range(len(lines)):
    #         line = "v%d %d %d\n" % (i, randint(0,screen_x), randint(0,screen_y))
    #         #f.write(line)
    #
    #         cities = line.split(' ', 2)
    #         print("%s" %cities)
    #
    #     #draw_scene()
    #
    # except IndexError:
    #     # aucun arguement
    #     print("Sans fichier")
    #     draw_scene()
    #     sys.exit(1)
    #
    # #draw_scene()
    #
    # f.close()