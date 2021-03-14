
import random
import time
import numpy as np
import tensorflow as tf
from pathfinder import *

random.seed()

class Board:
    decompose = True
    BOARDMAP = {
        'ground': 0,
        'snake': 1,
        'food': 2
    }

    def __init__(self, numsnakes=5, numfood=3, width=30, height=20):

        self.width = width
        self.height = height
        self.numsnakes = numsnakes
        self.numfood = numfood
        self.snakes = []
        self.deadsnakes = []
        self.food = []
        self.activegame = True

        self.board = np.zeros([self.height, self.width])

        self.initsnakes()
        self.initfood()
        self.updateboard()

    def initsnakes(self):
        for idx in range(self.numsnakes):
            self.updateboard()
            self.snakes.append(Snake(self.getvalidposition()))

    def initfood(self):
        for idx in range(self.numfood):
            self.updateboard()
            tempfood = Food(self.getvalidposition())
            self.food.append(tempfood)

    def updateboard(self):
        self.board = np.zeros([self.height, self.width])
        for snake in self.snakes:
            for cell in snake.body:
                self.board[cell[0]][cell[1]] = self.BOARDMAP['snake']
        for food in self.food:
            self.board[food.location[0]][food.location[1]] = self.BOARDMAP['food']

    def getvalidposition(self):
        valid_position = False
        position = []
        while not valid_position:
            position = [random.randrange(self.height), random.randrange(self.width)]
            valid_position = (self.board[position[0]][position[1]] == 0)
        return position

    def changedirection(self, dir):
        self.snakes[dir[0]].changedirection(dir[1])

    def updatesnakes(self):
        self.checkactivegame()
        if self.activegame:
            for snake in self.snakes:
                self.updateboard()
                snake.move(self.board)
                nextposition = snake.body[0]
                if self.wallcollision(nextposition):
                    snake.alive = False
                    self.snakes.remove(snake)
                else:
                    value = self.board[nextposition[0]][nextposition[1]]
                    if value == 1:
                        snake.alive = False
                        self.snakes.remove(snake)
                    elif value == 2:
                        self.popfood(nextposition)
                    else:
                        snake.noeat()
        else:
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
            if food.location == location:
                if food.respawnable:
                    tempfood = Food(self.getvalidposition())
                    self.food.append(tempfood)
                self.food.remove(food)


class Snake:
    DIRMAP = {
        'N': [-1, 0],
        'E': [0, 1],
        'S': [1, 0],
        'W': [0, -1]
    }

    def __init__(self, headpos, computer=True, name='snake', color='purple'):
        self.dir = list(self.DIRMAP.keys())[random.randrange(4)]
        self.speed = 1
        self.body = [headpos]
        self.alive = True
        self.computer = computer
        self.name = name
        self.color = color
        self.ticks = 0
        if self.computer:
            self.pathfinder = Pathfinder(self, BFS)

    def getposition(self):
        return self.body

    def changedirection(self, dir):
        if ((self.DIRMAP[dir][0] + self.DIRMAP[self.dir][0]) == 0) and ((self.DIRMAP[dir][1] + self.DIRMAP[self.dir][1]) == 0):
            self.dir = self.dir
        else:
            self.dir = dir

    def noeat(self):
        self.body.pop()

    def move(self, board):
        if self.computer:
            self.pathfinder.updatesnake(board)

        step = self.DIRMAP[self.dir]
        temp = [self.body[0][0], self.body[0][1]]
        temp[0] = temp[0] + step[0]
        temp[1] = temp[1] + step[1]
        self.body.insert(0, temp)
        self.ticks = self.ticks + 1

    def selfcollision(self):
        for idx in range(1, len(self.body)):
            if (self.body[0][0] == self.body[idx][0]) and (self.body[0][1] == self.body[idx][1]):
                return True
        else:
            return False


class Food:
    def __init__(self, location, respawnable=True):
        self.location = location
        self.respawnable = respawnable








