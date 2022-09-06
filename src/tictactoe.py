import sys
import pygame
from constants import *

from game import Game
from board import rowcol_to_move

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE")
screen.fill(BG_COLOR)


def main():

    game = Game(screen=screen)
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                col = pos[0] // SQSIZE
                row = pos[1] // SQSIZE
                move = rowcol_to_move(row, col)
                if board.is_empty_square(move.move) and game.running:
                    game.make_move(move)
                    if game.is_over():
                        game.running = False
                        print(f"Final state.")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and board.moveLog:
                    for _ in range(2 if game.gameMode == "AI" else 1):
                        undoMove, _ = game.board.moveLog[-1]
                        board.undo()
                        game.undo_X_O(undoMove)
                        game.update_player()
                        print(bin(board.squares)[2:].zfill(9))
                        game.running = True

                if event.key == pygame.K_g:
                    game.change_gamemode()

                if event.key == pygame.K_0:
                    ai.level = 0

                if event.key == pygame.K_1:
                    ai.level = 1

                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

        if game.gameMode == "AI" and game.player == ai.player and game.running:
            pygame.display.update()

            move = ai.eval(board)
            game.make_move(move)
            print(bin(board.squares)[2:].zfill(9))

            if game.is_over():
                game.running = False
                print(f"Final state.")

        pygame.display.update()


main()
