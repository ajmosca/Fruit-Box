import pygame
import sys
import button as button
from game import *

def playgame():
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or quitButton.drawButton(screen):
                pygame.quit()
                sys.exit()
            game.Events(event)

            if (resetButton.drawButton(screen) or playAgainButton.drawButton(screen)):
                game = Game()

        game.draw(screen)
        game.timer(screen)
        game.textdraw(screen)
        
        resetButton.active = not game.gameOver
        playAgainButton.active = game.gameOver
        quitButton.active = game.gameOver

        if game.gameOver:
            playAgainButton.drawButton(screen)
            quitButton.drawButton(screen)
        else:
            resetButton.drawButton(screen)

        pygame.display.flip()
        clock.tick(FPS)

playgame()
