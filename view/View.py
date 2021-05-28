import pygame
from model import model
from colors import *

FPS = 60


class View:
    """ View class is responsible to show the object on the screen
    :param
    :return:
    """

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((900, 500))
        self.win.fill(BLACK)
        self.base_font = pygame.font.SysFont('Corbel', 15)
        self.small_font = pygame.font.SysFont('Corbel', 35)
        pygame.display.set_caption("Simon Says")

    def update_view(self):
        """ Reset the screen, paint it all the to base color
        :param
        :return:
        """
        self.win.fill(BLACK)

    def show_window(self, objects):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param objects : an array of object that we can show on the screen. Can be only Text or Square isntace.
        :return:
        """
        for object_to_show in objects:
            if isinstance(object_to_show, model.Square):
                self.show_square(object_to_show)
            elif isinstance(object_to_show, model.Text):
                self.show_text(object_to_show)

    def show_square(self, square):
        """ shows Square object on the screen
        :param square: can be Square only
        :return:
        """

        if isinstance(square, model.Button):
            rect = self.get_rect_from_square(square)
            if square.text is not None:
                text = self.small_font.render(square.text, True, WHITE)
                rect.width = max(rect.width, text.get_width() + 45)
                pygame.draw.rect(self.win, square.color, rect)
                self.win.blit(text, (square.text_positionX, square.text_positionY))
            else:
                pygame.draw.rect(self.win, square.color, rect)
        else:
            rect = self.get_rect_from_square(square)
            pygame.draw.rect(self.win, square.color, rect)
        pygame.display.update()

    def show_text(self, txt):
        """ Shows Text object on the screen
        :param txt: An Text typed object.
        :return:
        """
        if txt.small is True:
            text = self.base_font.render(txt.msg, True, WHITE)
        else:
            text = self.small_font.render(txt.msg, True, WHITE, )
        self.win.blit(text, (txt.x, txt.y))
        pygame.display.update()

    def get_rect_from_square(self, square):
        """ This function getting Square object and returns Pygame.Rect
        :param square: Square object
        :return: pygame.Rect
        """
        return pygame.Rect(square.position[0], square.position[1], square.width, square.height)
