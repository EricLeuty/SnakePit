from queue import Queue
import numpy as np
from snake import *


class Pathfinder:

    def __init__(self, snake, method):
        self.snake = snake
        self.method = method
        self.path = []
        self.activepath = False

    def updatesnake(self, board):
        self.checkpath(board)
        if not self.activepath:
            self.findpath(board)
        head = np.asarray(self.snake.body[0])
        try:
            next = self.path[-1]
            step = next - head
            self.changedirection(step)
            self.path.pop()
        except IndexError:
            pass

    def findpath(self, board):
        head = self.snake.body[0]
        self.path = self.method(board).findpath(head)

    def changedirection(self, step):
        if np.all(step == [-1, 0]):
            self.snake.changedirection('N')
        elif np.all(step == [0, 1]):
            self.snake.changedirection('E')
        elif np.all(step == [1, 0]):
            self.snake.changedirection('S')
        elif np.all(step == [0, -1]):
            self.snake.changedirection('W')

    def checkpath(self, board):
        self.activepath = True
        if len(self.path) == 0:
            self.activepath = False
        else:
            target = self.path[0]
            if(board[target[0]][target[1]] == 2):
                for cell in self.path:
                    if board[cell[0]][cell[1]] == 1:
                        self.activepath = False
            else:
                self.activepath = False


class BFS:
    def __init__(self, board):
        self.queue = Queue(maxsize=0)
        self.visited = np.zeros((board.shape + (3,)), dtype=int)
        self.board = board
        self.path = []

    def findpath(self, head):
        target = self.findtarget(head)
        if target is None:
            neighbors = self.findneighbors(np.asarray(head))
            for n in neighbors:
                if self.board[n[0]][n[1]] != 1:
                    self.path.append(n)

        else:
            while (self.visited[target[0]][target[1]][1] != target[0]) or (self.visited[target[0]][target[1]][2] != target[1]):
                self.path.append(target)
                row = self.visited[target[0]][target[1]][1]
                col = self.visited[target[0]][target[1]][2]
                target = [row, col]
        return self.path

    def findtarget(self, head):
        head = np.asarray(head)
        self.visited[head[0]][head[1]][0] = 1
        self.visited[head[0]][head[1]][1] = head[0]
        self.visited[head[0]][head[1]][2] = head[1]
        self.queue.put(head)
        while not self.queue.empty():
            v = self.queue.get()
            if self.board[v[0]][v[1]] == 2:
                return v
            if (self.board[v[0]][v[1]] != 1) or (np.all(v == head)):
                neighbors = self.findneighbors(v)
                for n in neighbors:
                    if self.visited[n[0]][n[1]][0] == 0:
                        self.visited[n[0]][n[1]][0] = 1
                        self.visited[n[0]][n[1]][1] = v[0]
                        self.visited[n[0]][n[1]][2] = v[1]
                        self.queue.put(n)

    def findneighbors(self, v):
        neighbors = []
        n1 = v + [1, 0]
        n2 = v + [0, 1]
        n3 = v + [-1, 0]
        n4 = v + [0, -1]

        if self.inbounds(n1):
            neighbors.append(n1)
        if self.inbounds(n2):
            neighbors.append(n2)
        if self.inbounds(n3):
            neighbors.append(n3)
        if self.inbounds(n4):
            neighbors.append(n4)

        return neighbors

    def inbounds(self, n):
        return (0 <= n[0] < self.board.shape[0]) and (0 <= n[1] < self.board.shape[1])