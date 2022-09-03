from typing import Optional
import pygame
from ai import AI
from constants import *
from board import Board


class Game:
    def __init__(self, screen: pygame.Surface):
        self.board = Board()
        self.ai = AI()
        self.screen = screen
        self.player = 1  # 1 = x, -1 = o
        self.gameMode = "AI"  # "AI" or "PVP"
        self.running = True
        self.winLines = [
            lambda x: ((20, (2 * x + 1) * SQSIZE // 2), (WIDTH - 20, (2 * x + 1) * SQSIZE // 2)),
            lambda y: (((2 * y + 1) * SQSIZE // 2, 20), ((2 * y + 1) * SQSIZE // 2, HEIGHT - 20)),
            lambda x: ((20, 20), (WIDTH - 20, HEIGHT - 20)),
            lambda x: ((20, HEIGHT - 20), (WIDTH - 20, 20)),
        ]
        self.show_lines()

    def show_lines(self):
        """Draw the horizontal and vertical lines on the tic-tac-toe board."""

        self.screen.fill(BG_COLOR)

        pygame.draw.line(self.screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * SQSIZE, 0), (2 * SQSIZE, HEIGHT), LINE_WIDTH)

        pygame.draw.line(self.screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (0, 2 * SQSIZE), (WIDTH, 2 * SQSIZE), LINE_WIDTH)

    def update_player(self):
        """Change the player once a move has been made."""
        self.player *= -1

    def draw_X_O(self, row: int, col: int):
        """Draw either an X or an O depending on the player who made the current mark at row and col.

        Args:
            row (int): The row of the box where the mark is to be drawn.
            col (int): The column of the box where the mark is to be drawn.
        """
        if self.player == 1:
            pygame.draw.line(
                self.screen,
                CROSS_COLOR,
                (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET),
                ((col + 1) * SQSIZE - OFFSET, (row + 1) * SQSIZE - OFFSET),
                CROSS_WIDTH,
            )
            pygame.draw.line(
                self.screen,
                CROSS_COLOR,
                ((col + 1) * SQSIZE - OFFSET, row * SQSIZE + OFFSET),
                (col * SQSIZE + OFFSET, (row + 1) * SQSIZE - OFFSET),
                CROSS_WIDTH,
            )
        elif self.player == -1:
            pygame.draw.circle(
                self.screen,
                CIRCLE_COLOR,
                ((2 * col + 1) * SQSIZE / 2, (2 * row + 1) * SQSIZE / 2),
                CIRCLE_RADIUS,
                CIRCLE_WIDTH,
            )

    def undo_X_O(self, row: int, col: int):
        """Undo the previous marking.

        Args:
            row (int): The row of the box where the mark is to be drawn.
            col (int): The column of the box where the mark is to be drawn.
        """
        pygame.draw.rect(
            self.screen,
            BG_COLOR,
            pygame.Rect(
                col * SQSIZE + OFFSET / 2,
                row * SQSIZE + OFFSET / 2,
                SQSIZE - OFFSET,
                SQSIZE - OFFSET,
            ),
        )

    def make_move(self, row: int, col: int):
        """Make a move.

        Args:
            row (int): The row of the box where the mark is to be drawn.
            col (int): The column of the box where the mark is to be drawn.
        """
        self.board.mark_square(row, col, self.player)
        self.draw_X_O(row, col)
        self.update_player()

    def change_gamemode(self):
        """Change the game mode between player vs player (PVP) and player vs AI (AI)."""
        self.gameMode = "PVP" if self.gameMode == "AI" else "AI"

    def reset(self):
        """Reset the game."""
        self.__init__(self.screen)

    def is_over(self) -> bool:
        """Check whether the game is over.

        Returns:
            bool: Whether the game is over.
        """
        status = self.board.final_state()
        if status is not None:
            self.draw_win_lines(status)
        return self.board.final_state() is not None

    def draw_win_lines(self, status: Optional[int]):
        """Draw a line along the winning row (or column or diagonal) once the
        game is over."""
        color = CIRCLE_COLOR if status == -1 else CROSS_COLOR
        for i, x in enumerate(self.board.whereWin):
            if x is not None:
                pygame.draw.line(self.screen, color, *self.winLines[i](x), LINE_WIDTH)
