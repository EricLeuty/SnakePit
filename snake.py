
import random
import time
import numpy as np
import tensorflow as tf

random.seed()


class Constants:
    DECOMPOSE = True

    DIRMAP = {
        'N': [-1, 0],
        'E': [0, 1],
        'S': [1, 0],
        'W': [0, -1]
    }



class Board:
    def __init__(self, numsnakes=2, width=30, height=20):

        self.width = width
        self.height = height
        self.numsnakes = numsnakes
        self.snakes = []
        self.food = []
        self.activegame = True

        board = tf.zeros([self.height, self.width], tf.int8)
        self.board = board

        self.initsnakes()
        self.placefood()

    def changedirection(self, dir):
        self.snakes[dir[0]].changedirection(dir[1])

    def initsnakes(self):
        for idx in range(self.numsnakes):
            self.snakes.append(Snake(self.placenocollision()))

    def updatesnake(self):
        if self.activegame:
            for snake in self.snakes:
                snake.move()
                self.foodcollision(snake)
                if self.snakecollision(snake) or self.wallcollision(snake):
                    snake.alive = False
            self.checkactivegame()
        else:
            print("Game Over!")

    def checkactivegame(self):
        snakealive = False
        for snake in self.snakes:
            snakealive = (snakealive or snake.alive)
        self.activegame = snakealive

    def placenocollision(self):
        valid_position = False
        position = []
        while not valid_position:
            position = [random.randrange(self.height), random.randrange(self.width)]
            valid_position = True
            for snake in self.snakes:
                for cell in snake.body:
                    if position == cell:
                        valid_position = False
        return position

    def placefood(self):
        self.food.append(self.placenocollision())

    def wallcollision(self, currentsnake):
        head = currentsnake.body[0]
        return (head[0] < 0) or (head[0] >= self.height) or (head[1] < 0) or (head[1] >= self.width)

    def snakecollision(self, currentsnake):
        head = currentsnake.body[0]
        collision = False
        for snake in self.snakes:
            if snake is currentsnake:
                collision = collision or snake.selfcollision()
            else:
                for cell in snake.body:
                    if cell == head:
                        collision = True
        return collision

    def foodcollision(self, currentsnake):
        head = currentsnake.body[0]
        for food in self.food:
            if head == food:
                self.food.remove(food)
                self.placefood()
                return True
        currentsnake.noeat()
        return False


class Snake:
    def __init__(self, startpos, name='snake', color='purple'):
        self.dir = list(Constants.DIRMAP.keys())[random.randrange(4)]
        self.speed = 1
        self.body = [startpos]
        self.alive = True
        self.name = name
        self.color = color
        self.ticks = 0

    def getposition(self):
        return self.body

    def changedirection(self, dir):
        if ((Constants.DIRMAP[dir][0] + Constants.DIRMAP[self.dir][0]) == 0) and ((Constants.DIRMAP[dir][1] + Constants.DIRMAP[self.dir][1]) == 0):
            self.dir = self.dir
        else:
            self.dir = dir

    def noeat(self):
        self.body.pop()

    def move(self):
        step = Constants.DIRMAP[self.dir]
        temp = [self.body[0][0], self.body[0][1]]
        temp[0] = temp[0] + step[0]
        temp[1] = temp[1] + step[1]
        self.body.insert(0, temp)

    def selfcollision(self):
        for idx in range(1, len(self.body)):
            if (self.body[0][0] == self.body[idx][0]) and (self.body[0][1] == self.body[idx][1]):
                return True
        else:
            return False

    def addtick(self):
        self.ticks = self.ticks + 1


