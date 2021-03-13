from tkinter import *
from snake import *

class Constants:
    SIZE = 20
    DELAY = 100
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

def test():
    root = Tk()
    g = Game()
    root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()
