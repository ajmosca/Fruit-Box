import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.active = True

    def drawButton(self, surface):
        if not self.active:
            return False

        action = False

        pos = pygame.mouse.get_pos()
        surface.blit(self.image, (self.rect.x, self.rect.y))

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
    
        elif pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        if self.clicked and pygame.mouse.get_pressed()[0] == 0 and self.rect.collidepoint(pos):
            action = True
            self.clicked = False

        return action
