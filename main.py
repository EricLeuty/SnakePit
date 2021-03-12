from tkinter import *
import random
import time
import numpy as np

random.seed()

class Constants:
    SIZE = 20
    DELAY = 100
    DECOMPOSE = True
    KEYMAP = {
        'w': 'N',
        'd': 'E',
        's': 'S',
        'a': 'W'
    }
    KEYMAP2P = {
        'w': [0, 'N'],
        'd': [0, 'E'],
        's': [0, 'S'],
        'a': [0, 'W'],
        'Up': [1, 'N'],
        'Right': [1, 'E'],
        'Down': [1, 'S'],
        'Left': [1, 'W']
    }
    DIRMAP = {
        'N': [-1, 0],
        'E': [0, 1],
        'S': [1, 0],
        'W': [0, -1]
    }
    COLORMAP = {
        0: "lawn green",
        1: "purple",
        2: "yellow"
    }


class Game(Frame):
    def __init__(self):
        super().__init__()

        self.master.title("Snake")

        self.window = Window()
        self.window.grid(row=0, column=0)
        self.scorelabel = Label(text='')
        self.scorelabel.grid(row=1, column=0, sticky='w')
        self.updatescore()

    def updatescore(self):
        self.scorelabel.config(text=("Score: " + str(len(self.window.board.snakes[0].body))))
        self.scorelabel.after(Constants.DELAY, self.updatescore)


class Window(Canvas):
    def __init__(self, width=40, height=30):
        super().__init__(width=(width * Constants.SIZE), height=(height * Constants.SIZE), background="green",
                         bd=1)

        self.board = Board(2, width, height)
        self.bind_all('<Key>', self.changedirection)
        self.after(Constants.DELAY, self.updategame)
        self.pack()

    def updategame(self):
        if self.board.activegame:
            self.board.updatesnake()
            self.printboard()
            self.after(Constants.DELAY, self.updategame)
        else:
            print("Game Over!")

    def changedirection(self, event):
        try:
            self.board.changedirection(Constants.KEYMAP2P[event.keysym])
        except KeyError:
            exit()

    def printboard(self):
        self.delete("all")
        self.printsnake()
        self.printfood()

    def printsnake(self):
        for snake in self.board.snakes:
            for cell in snake.body:
                y = Constants.SIZE*cell[0]
                x = Constants.SIZE*cell[1]
                self.create_rectangle(x, y, (x + Constants.SIZE), (y + Constants.SIZE), fill=snake.color)

    def printfood(self):
        for food in self.board.food:
            y = Constants.SIZE * food[0]
            x = Constants.SIZE * food[1]
            self.create_rectangle(x, y, (x + Constants.SIZE), (y + Constants.SIZE), fill=Constants.COLORMAP[2])


class Board:
    def __init__(self, numsnakes=2, width=30, height=20):

        self.width = width
        self.height = height
        self.numsnakes = numsnakes
        self.snakes = []
        self.food = []
        self.activegame = True
        self.addsnakes()
        self.placefood()

    def changedirection(self, dir):
        self.snakes[dir[0]].changedirection(dir[1])

    def addsnakes(self):
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
        self.dir = Constants.KEYMAP[list(Constants.KEYMAP.keys())[random.randrange(4)]]
        self.speed = 1
        self.body = [startpos]
        self.alive = True
        self.name = name
        self.color = color

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


def test():
    root = Tk()
    g = Game()
    root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()
