import sys
import pygame
from constants import *

from game import Game

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

                if board.is_empty_square(row, col) and game.running:
                    game.make_move(row, col)
                    
                    if game.is_over():
                        game.running = False
                        print(f"Final state.")
                    
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and board.moveLog:
                    for _ in range(2 if game.gameMode=="AI" else 1):
                        undo_row, undo_col = board.undo()
                        game.undo_X_O(undo_row, undo_col)
                        game.update_player()
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
            
            row, col = ai.eval(board)            
            game.make_move(row, col)
            
            if game.is_over():
                game.running = False
                print(f"Final state.")

        pygame.display.update()


main()
