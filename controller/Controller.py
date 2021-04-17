import pygame
from model import model
from colors import *


class Controller:
    def __init__(self, view):
        self.keepGoing = True
        self.view = view

    def run(self):
        clock = pygame.time.Clock()
        while self.keepGoing:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.keepGoing = False

            event_pos = self.get_event()
            self.init_window(event_pos)

    def init_window(self,event_pos):
        square1 = model.Square(30, (450, 250), RED)
        if square1.get_rect().collidepoint(event_pos):
            square1.update_color(YELLOW)

        self.view.show_window([square1])

    def get_event(self):
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                return pygame.mouse.get_pos()

        return None
