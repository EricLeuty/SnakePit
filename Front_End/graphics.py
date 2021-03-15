import sys

sys.path.insert(1, '/home/eric/PycharmProjects/SnakePit/Back_End')
from _thread import *
from tkinter import *
from snake import *
from network import Network


class Constants:
    SIZE = 20
    DELAY = 5
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
        2: "yellow",
        3: "grey"
    }


class Game(Frame):
    def __init__(self):
        super().__init__()

        self.master.title("Snake")
        self.currentplayer = "eric"

        self.window = Window()
        self.window.grid(row=0, column=0, columnspan=3)
        self.scorelabels = [[],[],[]]
        self.snakestats()
        self.updatescore()


    def updatescore(self):
        if self.window.board.activegame:
            self.window.printboard()
            for idx in range(len(self.window.board.snakes)):
                (name, length, ticks) = self.window.board.snakes[idx].getstats()
                self.scorelabels[idx][0].config(text=name)
                self.scorelabels[idx][1].config(text=length)
                self.scorelabels[idx][2].config(text=ticks)
            self.scorelabels[idx][0].after(Constants.DELAY, self.updatescore)
        else:
            pass

    def snakestats(self):
        for idx in range(len(self.window.board.snakes)):
            self.scorelabels[idx].append(Label(text=''))
            self.scorelabels[idx][0].grid(row=idx+1, column=0, sticky='w')
            self.scorelabels[idx].append(Label(text=''))
            self.scorelabels[idx][1].grid(row=idx + 1, column=1, sticky='w')
            self.scorelabels[idx].append(Label(text=''))
            self.scorelabels[idx][2].grid(row=idx + 1, column=2, sticky='w')



class Window(Canvas):
    def __init__(self, width=30, height=20):
        super().__init__(width=((width + 2) * Constants.SIZE), height=((height + 2) * Constants.SIZE), background="green",
                         bd=1)



        self.board = Board(width=width, height=height)

        self.pack()

    def changedirection(self, event):
        try:
            dir = Constants.KEYMAP[event.keysym]

            self.printboard()
        except KeyError:
            exit()

    def printboard(self):
        self.delete("all")
        (rows, cols) = self.board.board.shape
        for row in range(rows):
            for col in range(cols):
                if self.board.board[row][col] != 0:
                    y = Constants.SIZE * row
                    x = Constants.SIZE * col
                    self.create_rectangle(x, y, (x + Constants.SIZE), (y + Constants.SIZE), fill=Constants.COLORMAP[self.board.board[row][col]])



def test():
    n = Network()
    root = Tk()
    g = Game()
    root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()
