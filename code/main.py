import pygame
import asyncio
import sys
from game import *

async def playgame():
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or quitButton.drawButton(screen):
                running = False
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

        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(playgame())
