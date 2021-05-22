import pygame
from model import model
from colors import *

FPS = 60


class View:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((900, 500))
        self.win.fill(WHITE)
        self.small_font = pygame.font.SysFont('Corbel', 35)
        pygame.display.set_caption("Simon Says")

    def update_view(self):
        self.win.fill(WHITE)

    def show_window(self, objects):
        """Objets to show on the screen"""
        for object_to_show in objects:
            if isinstance(object_to_show, model.Square):
                self.show_square(object_to_show)
            elif isinstance(object_to_show, model.Text):
                self.show_text(object_to_show)

    def show_square(self, square):
        """Show on square"""
        rect = self.get_rect_from_square(square)
        pygame.draw.rect(self.win, square.color, rect)
        if isinstance(square, model.Button):
            if square.text is not None:
                text = self.small_font.render(square.text, True, WHITE)
                self.win.blit(text, (square.text_positionX, square.text_positionY))
        pygame.display.update()

    def show_text(self, txt):
        """Shows text on the screen"""
        text = self.small_font.render(txt.msg, True, BLACK)
        self.win.blit(text, (txt.x, txt.y))
        pygame.display.update()

    def get_rect_from_square(self, square):
        return pygame.Rect(square.position[0], square.position[1], square.width, square.height)
