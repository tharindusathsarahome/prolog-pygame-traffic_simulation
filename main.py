import random
import time
import threading
import pygame
import sys
from pyswip import Prolog
import math

prolog = Prolog()


speeds = {'car': 4.5, 'bus': 2, 'truck': 2, 'bike': 7}

vehicleTypes = {0: 'car', 1: 'bike', 2: 'bus', 3: 'truck'}

stoppingGap = 15
movingGap = 30

pygame.init()
simulation = pygame.sprite.Group()


movePoints = {
    'a': (0, 60),
    'b': (137, 60),
    'c': (225, 60),
    'd': (380, 60),
    'e': (540, 60),
    'f': (55, 200),
    'g': (137, 200),
    'h': (225, 200),
    'i': (380, 200),
    'j': (540, 200),
    'k': (165, 308),
    'l': (342, 308),
    'm': (585, 308),
    'n': (0, 510),
    'o': (55, 510),
    'p': (165, 510),
    'q': (342, 510),
    'r': (585, 510),
    's': (540, 308),
    't': (700, 60),
    'u': (700, 510),
    'v': (450, 510),
    'w': (342, 665),
    'x': (450, 665),
    'y': (565, 665),
    'z': (565, 510),
}

paths = [
     ['n', 'o', 'right', 0],
     ['o', 'f', 'up', 0],
     ['o', 'p', 'right', 0],
     ['f', 'g', 'right', 0],
     ['a', 'b', 'right', 0],
     ['b', 'g', 'down', 0],
     ['b', 'c', 'right', 0],
     ['c', 'h', 'down', 0],
     ['g', 'h', 'right', 0],
     ['p', 'k', 'up', 0],
     ['p', 'q', 'right', 0],
     ['k', 'l', 'right', 0],
     ['q', 'l', 'up', 0],
     ['h', 'i', 'right', 0],
     ['i', 'd', 'up', 0],
     ['i', 'j', 'right', 0],
     ['d', 'e', 'right', 0],
     ['j', 's', 'down', 0],
     ['l', 's', 'right', 0],
     ['s', 'm', 'right', 0],
     ['m', 'r', 'down', 0],
     ['e', 't', 'right', 0],
     ['r', 'u', 'right', 0],
     ['q', 'v', 'right', 0],
     ['q', 'w', 'down', 0],
     ['w', 'x', 'right', 0],
     ['v', 'x', 'down', 0],
     ['x', 'y', 'right', 0],
     ['y', 'z', 'up', 0],
     ['z', 'r', 'right', 0],
     ['j', 'e', 'up', 0],
     ['s', 'j', 'up', 0],
     ['g', 'f', 'left', 0],
     ['f', 'o', 'down', 0]
     ]

def distance(point1, point2):
    x1, y1 = movePoints[point1]
    x2, y2 = movePoints[point2]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, vehicleClass, startPoint, endPoint):
        pygame.sprite.Sprite.__init__(self)
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.startPoint = startPoint
        self.endPoint = endPoint

        self.config()

        simulation.add(self)

    def config(self):
        try:
            with open("prolog.pl", "r") as prolog_file:
                lines = prolog_file.readlines()[:21]
                with open("temp.pl", "w+") as prolog_file:
                    prolog_file.writelines(lines)

            with open("temp.pl", "a") as prolog_file:
                for path in paths:
                    dist = distance(path[0], path[1]) / 25
                    # traffic = int(path[3] / dist * 100)
                    fact = f"road({path[0]}, {path[1]}, {int(dist)}, {path[3]}).\n"
                    prolog_file.write(fact)

            prolog.consult("temp.pl")

            query = "shortest_path({}, {}, Path, Length, Traffic)".format(self.startPoint, self.endPoint)
            result = list(prolog.query(query))

            print(list(prolog.query(f"setof([T, L, P], find_path({self.startPoint}, {self.endPoint}, P, L, T), Paths)")))

            if not result or not result[0]:
                self.kill()
                return

            self.route, _, _ = result[0]["Path"], result[0]["Length"], result[0]["Traffic"]

            self.x, self.y = movePoints[str(self.route[0])]

            for item in paths:
                if item[0] == str(self.route[0]) and item[1] == str(self.route[1]):
                    self.direction = item[2]
                    item[3] += 1
                if item[0] == str(self.route[1]) and item[1] == str(self.route[0]):
                    item[3] += 1

            path = "images/" + self.direction + "/" + self.vehicleClass + ".png"
            originalImage = pygame.image.load(path)

            o_w, o_h = originalImage.get_size()
            self.image = pygame.transform.scale(originalImage, (int(o_w * 0.6), int(o_h * 0.6)))


        except Exception as e:
            print(e)
            self.config()


    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        x, y = movePoints[str(self.route[1])]

        if(self.direction == 'right'):
            if(self.x <= x):
                for vehicle in simulation: 
                    if vehicle != self:
                        if self.x + self.image.get_rect().width + stoppingGap >= vehicle.x and self.x + self.image.get_rect().width + stoppingGap < vehicle.x + movingGap and self.y == vehicle.y:
                            break
                else:
                    self.x += self.speed
            else:
                for item in paths:
                    if item[0] == str(self.route[0]) and item[1] == str(self.route[1]):
                        item[3] -= 1
                    if item[0] == str(self.route[1]) and item[1] == str(self.route[0]):
                        item[3] -= 1
                self.startPoint = self.route[1]
                self.config()
        elif(self.direction == 'down'):
            if(self.y <= y):
                for vehicle in simulation: 
                    if vehicle != self:
                        if self.y + self.image.get_rect().height + stoppingGap >= vehicle.y and self.y + self.image.get_rect().height + stoppingGap < vehicle.y + movingGap and self.x == vehicle.x:
                            break
                else:
                    self.y += self.speed
            else:
                for item in paths:
                    if item[0] == str(self.route[0]) and item[1] == str(self.route[1]):
                        item[3] -= 1
                    if item[0] == str(self.route[1]) and item[1] == str(self.route[0]):
                        item[3] -= 1
                self.startPoint = self.route[1]
                self.config()
        elif(self.direction == 'up'):
            if(self.y >= y):
                for vehicle in simulation: 
                    if vehicle != self:
                        if self.y - stoppingGap - vehicle.image.get_rect().height <= vehicle.y and self.y - stoppingGap - vehicle.image.get_rect().height > vehicle.y - movingGap and self.x == vehicle.x:
                            break
                else:
                    self.y -= self.speed
            else:
                for item in paths:
                    if item[0] == str(self.route[0]) and item[1] == str(self.route[1]):
                        item[3] -= 1
                    if item[0] == str(self.route[1]) and item[1] == str(self.route[0]):
                        item[3] -= 1
                self.startPoint = self.route[1]
                self.config()
        elif(self.direction == 'left'):
            if(self.x >= x):
                self.x -= self.speed
            else:
                for item in paths:
                    if item[0] == str(self.route[0]) and item[1] == str(self.route[1]):
                        item[3] -= 1
                    if item[0] == str(self.route[1]) and item[1] == str(self.route[0]):
                        item[3] -= 1
                self.startPoint = self.route[1]
                self.config()

def initialize_vehicles():
    i = 0
    while(True):
        print(len(simulation))
        if (len(simulation) < 15):
            startLane = ['a','n'][random.randint(0, 1)]
            endLane = ['u','t'][random.randint(0, 1)]
            vehicleType = vehicleTypes[2 if i < 6 else 1 if i < 12 else random.randint(0, 2)]
            Vehicle(vehicleType, startLane, endLane)
            i+=1
        time.sleep(2)

# Main loop
class Main:
    thread = threading.Thread(name="initialize_vehicles", target=initialize_vehicles)
    thread.daemon = True
    thread.start()

    # Screensize
    screenWidth = 700
    screenHeight = 700
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/intersection.png')
    background = pygame.transform.scale(background, screenSize)

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at position:", (mouse_x, mouse_y))
                print(paths)
                for vehicle in simulation:
                    if vehicle.x < mouse_x < vehicle.x + vehicle.image.get_rect().width and vehicle.y < mouse_y < vehicle.y + vehicle.image.get_rect().height:
                        for item in paths:
                            if item[0] == str(vehicle.route[0]) and item[1] == str(vehicle.route[1]):
                                item[3] -= 1
                            if item[0] == str(vehicle.route[1]) and item[1] == str(vehicle.route[0]):
                                item[3] -= 1
                        vehicle.kill()
                        break

        screen.blit(background, (0, 0))
                
        for vehicle in simulation:  
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move()

        pygame.display.update()