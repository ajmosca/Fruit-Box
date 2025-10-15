import random
import pygame
import button as button

#variables
WIDTH, HEIGHT = 1450, 1000
GRID_COLS, GRID_ROWS = 17, 10
CELL_SIZE = 80
GRID_ORIGIN = (50, 50)
RESETBUTTONCOORDS = (1000, 900)
PLAYAGAINBUTTONCOORDS = (570, 700)

FPS = 60

BG = (204, 255, 204)
GRID_BG = (232, 255, 230)
GAMEOVER_BG = (169, 169, 169)
BOX_COLOR = (0, 0, 255)
BOX_FILL_COLOR = (0, 0, 100)
TEXT_COLOR1 = (61, 5, 5)
TEXT_COLOR2 = (255, 0, 0)
GAMEOVER_COLOR = (0, 0, 0)
GAMEOVERBOX_COLOR = (255, 255, 255)

TIMELIMIT = 90

#pygame start functions
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('EH box')
clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsansms", 28)
timerfont = pygame.font.SysFont("comicsansms", 40)

#Load images and SFX
imagePath1 = "images\\eh1.png"
imagePath2 = "images\\eh2.png"
imagePath3 = "images\\eh3.png"
eh1 = pygame.image.load(imagePath1).convert_alpha()
eh2 = pygame.image.load(imagePath2).convert_alpha()
eh3 = pygame.image.load(imagePath3).convert_alpha()

cryehPath = "images\\cryeh.webp"
okehPath = "images\\okeh.webp"
cryehImage = pygame.image.load(cryehPath).convert_alpha()
okehImage = pygame.image.load(okehPath).convert_alpha()

resetImagepath = "images\\Reset.png"
playAgainImagepath = "images\\PlayAgain.png"
quitImagepath = "images\\Quit.png"
resetImage = pygame.image.load(resetImagepath).convert_alpha()
playAgainImage = pygame.image.load(playAgainImagepath).convert_alpha()
quitImage = pygame.image.load(quitImagepath).convert_alpha()

gameoverSound = pygame.mixer.Sound('soundEffects\\deltarune-explosion.mp3')
popSound = pygame.mixer.Sound('soundEffects\\pop-402323.mp3')

resetButton = button.Button(RESETBUTTONCOORDS[0], RESETBUTTONCOORDS[1], resetImage, 1)
playAgainButton = button.Button(PLAYAGAINBUTTONCOORDS[0], PLAYAGAINBUTTONCOORDS[1], playAgainImage, 1)
quitButton = button.Button(PLAYAGAINBUTTONCOORDS[0], PLAYAGAINBUTTONCOORDS[1] + 100, quitImage, 1)

class Game:
    def __init__(self):

        self.board = [[random.randint(1,3) for _ in range(GRID_COLS)] for _ in range (GRID_ROWS)]
        
        self.dragging = False
        self.startPosition = None
        self.currRectangle = None
        self.score = 0
        self.gameOver = False
        self.startTime = pygame.time.get_ticks()

    def GridToScreen(self, row, col):
        x0, y0 = GRID_ORIGIN
        return x0 + col * CELL_SIZE, y0 + row * CELL_SIZE
    
    def Events(self, event):
        #If timer runs out, stop inputs.
        if self.gameOver:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.dragging = True
                self.startPosition = event.pos
                self.currRectangle = pygame.Rect(event.pos, (0,0))

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                x0, y0 = self.startPosition
                x1, y1 = event.pos
                xmin= min(x0, x1)
                ymin = min(y0, y1)
                width = abs(x1 - x0)
                height = abs(y1 - y0)
                self.currRectangle = pygame.Rect(xmin, ymin, width, height)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                self.dragging = False
                self.checkSelection()
                self.currRectangle = None        

    def checkSelection(self):
        #Checks if the current selection rectangle goes over cells with numbers, and checks to see if its a valid sum of 10
        if self.currRectangle is None:
            return
        
        selected = []
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                num = self.board[r][c]
                if num is None:
                    continue
                sx, sy = self.GridToScreen(r,c)
                center = (sx + CELL_SIZE/2, sy + CELL_SIZE/2)
                if self.currRectangle.collidepoint(center):
                    selected.append((r, c, num))
                    
        if not selected:
            return
        
        total = sum(num for (_, _, num) in selected)
        if total == 10:
            popSound.play()
            for (r, c, _) in selected:
                self.board[r][c] = None
            self.score += len(selected) #*10 #for testing
            print(self.score)
    
    def draw(self, surface):
        #Draws the game onto the screen
        surface.fill(BG)

        x0, y0 = GRID_ORIGIN
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                sx = x0 + c*CELL_SIZE
                sy = y0 + r*CELL_SIZE
                rectangle = pygame.Rect(sx, sy, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, GRID_BG, rectangle)
                pygame.draw.rect(surface, (100, 100, 100), rectangle, 1)
                num = self.board[r][c]
                if num is not None:
                    if num == 1:
                        surface.blit(eh1, (sx + 3, sy + 3))
                    if num == 2:
                        surface.blit(eh2, (sx + 3, sy + 3))
                    if num == 3:
                        surface.blit(eh3, (sx + 3, sy + 3))
        
        if self.gameOver:
            #draws gameover screen
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(GAMEOVER_BG)
            surface.blit(overlay, (0,0))

            gameoverRect = pygame.Rect(610, 450, 3 * CELL_SIZE, 2 * CELL_SIZE)
            pygame.draw.rect(surface, GAMEOVERBOX_COLOR, gameoverRect)
            pygame.draw.rect(surface, GAMEOVER_COLOR, gameoverRect, 5)

            if self.score <= 99:
                surface.blit(cryehImage, (
                    WIDTH // 2 - cryehImage.get_width() // 2, 300
                    ))
            else:
                surface.blit(okehImage, (
                    WIDTH // 2 - okehImage.get_width() // 2, 300
                ))

            gameoverText = font.render(" Game Over", True, GAMEOVER_COLOR)
            gameoverscoreText = font.render(f"Score: {self.score}", True, GAMEOVER_COLOR)
            surface.blit(gameoverText, (
                WIDTH // 2 - gameoverText.get_width() // 2, 
                HEIGHT // 2 - gameoverText.get_height() // 2
                ))
            surface.blit(gameoverscoreText, (
                WIDTH // 2 - gameoverscoreText.get_width() // 2,
                HEIGHT // 2 + gameoverscoreText.get_height()
            ))
        
        if self.currRectangle and not self.gameOver:
            pygame.draw.rect(surface, BOX_COLOR, self.currRectangle, 2)

    def textdraw(self, surface):
        if not self.gameOver:
            # render and draw score text
            scoretext = font.render("Score: ", True, TEXT_COLOR1)
            scoretext2 = font.render(f"{self.score}", True, TEXT_COLOR2)
            surface.blit(scoretext, (100,900))
            surface.blit(scoretext2, (185,900))

    def timer(self, surface):
        if self.gameOver:
            return
        #render and draw timer text when game is not in game over.
        currentTime = pygame.time.get_ticks()
        elapsedTime = currentTime - self.startTime
        remainingTime = TIMELIMIT - (elapsedTime / 1000) #converts from ms to s

        if remainingTime <= 0:
            if not self.gameOver:
                gameoverSound.play()
            
            self.gameOver = True
            remainingTime = 0
        
        timerText = font.render(f"Time Left: {int(remainingTime)}", True, TEXT_COLOR1)
        surface.blit(timerText, (WIDTH / 2 - timerText.get_width() // 2, 10))



