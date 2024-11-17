import pygame

pygame.init()

coolfont = pygame.font.Font("fonts/EncodeSansNarrow-Bold.ttf", 60)


class Button():
    def __init__(self, color, text_color, x, y, width, height, text=''):
        self.color = color
        self.text_color = text_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = coolfont.render(self.text, 1, (self.text_color))
            screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False
