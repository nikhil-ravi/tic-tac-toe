import pygame
from constants import *
import numpy as np


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_squares = self.squares
        self.marked_squares = 0
        self.rows = [0] * ROWS
        self.cols = [0] * COLS
        self.diag = 0
        self.antidiag = 0
        self.moveLog = []
        self.whereWin = [None, None, None, None]

    def final_state(self):
        if self.moveLog:
            row, col, player = self.moveLog[-1]
            toCheck = (self.rows[row], self.cols[col], self.diag, self.antidiag)
            for i, line in enumerate(toCheck):
                if abs(line) == ROWS:
                    if i == 0:
                        self.whereWin[i] = row
                    elif i == 1:
                        self.whereWin[i] = col
                    else:
                        self.whereWin[i] = True
                    return player
            if self.is_full():
                return 0
            else:
                return None
        else:
            return None

    def mark_square(self, row, col, player):
        self.moveLog.append((row, col, player))
        self.squares[row, col] = player
        self.marked_squares += 1
        self.rows[row] += player
        self.cols[col] += player
        if row == col:
            self.diag += player
        if row + col == ROWS - 1:
            self.antidiag += player
    
    def undo(self):
        row, col, player = self.moveLog.pop()
        self.squares[row, col] = 0
        self.marked_squares -= 1
        self.rows[row] -= player
        self.cols[col] -= player
        if row == col:
            self.diag -= player
        if row + col == ROWS - 1:
            self.antidiag -= player
        return row, col

    def is_empty_square(self, row, col):
        return self.squares[row, col] == 0

    def is_full(self):
        return self.marked_squares == 9

    def is_empty(self):
        return self.marked_squares == 0

    def get_empty_squares(self):
        return np.stack(np.where(self.squares == 0), axis=-1).tolist()
