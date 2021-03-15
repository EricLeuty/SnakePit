
import random
import time
import numpy as np
import tensorflow as tf
import csv
from pathfinder import *

random.seed()

class Board:
    decompose = True
    BOARDMAP = {
        'ground': 0,
        'snake': 1,
        'food': 2,
        'wall': 3
    }

    def __init__(self, numfood=1, width=30, height=20):

        self.width = width + 2
        self.height = height + 2
        self.numsnakes = 0
        self.numfood = numfood
        self.snakes = []
        self.deadsnakes = []
        self.food = []
        self.snakehash = {}
        self.activegame = True

        self.board = np.zeros([self.height, self.width])

        self.addsnakes([Snake(), Snake(), Snake()])
        self.initsnakes()
        self.initfood()
        self.updateboard()

    def addsnakes(self, snakes):
        num = 0
        for snake in snakes:
            if snake.computer:
                snake.name = "Snake" + str(num)
                num = num + 1
            self.snakes.append(snake)
            self.snakehash[snake.name] = snake
        self.numsnakes = len(snakes)

    def initsnakes(self):
        for snake in self.snakes:
            self.updateboard()
            snake.spawn(self.getvalidposition())

    def initfood(self):
        for idx in range(self.numfood):
            self.updateboard()
            tempfood = Food(self.getvalidposition())
            self.food.append(tempfood)

    def updateboard(self):
        self.board = np.zeros([self.height, self.width])
        self.board[0, :] = self.BOARDMAP['wall']
        self.board[:, -1] = self.BOARDMAP['wall']
        self.board[-1, :] = self.BOARDMAP['wall']
        self.board[:, 0] = self.BOARDMAP['wall']
        for snake in self.snakes:
            if snake.alive:
                for cell in snake.body:
                    self.board[tuple(cell)] = self.BOARDMAP['snake']
        for food in self.food:
            self.board[tuple(food.location)] = self.BOARDMAP['food']

    def getvalidposition(self):
        valid_position = False
        position = []
        while not valid_position:
            position = np.array([random.randrange(self.height), random.randrange(self.width)])
            valid_position = np.all(self.board[tuple(position)] == 0)
        return position

    def changedirection(self, dir):
        self.snakes[dir[0]].changedirection(dir[1])

    def updatesnakes(self):
        self.checkactivegame()
        if self.activegame:
            for snake in self.snakes:
                if snake.alive:
                    self.updateboard()
                    snake.move(self.board)
                    nextposition = snake.gethead()
                    value = self.board[tuple(nextposition)]
                    if value == 1 or value == 3:
                        snake.kill(self.board)

                    elif value == 2:
                        self.popfood(nextposition)
                    else:
                        snake.noeat()
            self.snakes.sort(key=lambda snake: len(snake.body), reverse=True)
        else:
            self.writesnakedata()
            print("Game Over!")

    def checkactivegame(self):
        snakealive = False
        for snake in self.snakes:
            snakealive = (snakealive or snake.alive)
        self.activegame = snakealive

    def wallcollision(self, nextposition):
        return (nextposition[0] < 0) or (nextposition[0] >= self.height) or (nextposition[1] < 0) or (nextposition[1] >= self.width)

    def popfood(self, location):
        for food in self.food:
            if np.all(food.location == location):
                if food.respawnable:
                    tempfood = Food(self.getvalidposition())
                    self.food.append(tempfood)
                self.food.remove(food)

    def writesnakedata(self):
        with open('snakedata.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Snake Name", "Length", "Ticks", "Deathstate"])
            for snake in self.snakes:
                (name, length, ticks) = snake.getstats()
                deathstate = snake.lastboard
                writer.writerow([name, length, ticks, deathstate])



class Snake:
    DIRMAP = {
        'N': np.array([-1, 0]),
        'E': np.array([0, 1]),
        'S': np.array([1, 0]),
        'W': np.array([0, -1])
    }

    def __init__(self, name='', computer=True, color='purple'):
        self.dir = list(self.DIRMAP.keys())[random.randrange(4)]
        self.speed = 1
        self.body = [np.array([0, 0])]
        self.alive = True
        self.computer = computer
        self.name = name
        self.color = color
        self.ticks = 0
        self.lastboard = []
        if self.computer:
            self.pathfinder = Pathfinder(self, BFS)

    def spawn(self, headpos):
        self.body[0] = np.array(headpos)

    def gethead(self):
        return self.body[0]

    def getposition(self):
        return self.body

    def changedirection(self, dir):
        if np.any(self.DIRMAP[dir] + self.DIRMAP[self.dir] == 0):
            self.dir = self.dir
        else:
            self.dir = dir

    def noeat(self):
        self.body.pop()

    def move(self, board):
        if self.computer:
            self.pathfinder.updatesnake(board)

        step = self.DIRMAP[self.dir]
        temp = self.body[0]
        temp = temp + step
        self.body.insert(0, temp)
        self.ticks = self.ticks + 1

    def kill(self, board):
        self.alive = False
        self.lastboard = board

    def getstats(self):
        return [self.name, str(len(self.body)), str(self.ticks)]


class Food:
    def __init__(self, location, respawnable=True):
        self.location = location
        self.respawnable = respawnable








