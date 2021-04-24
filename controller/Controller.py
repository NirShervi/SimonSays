import pygame
from model import model
from colors import *
from threading import Timer


class Controller:
    def __init__(self, view):
        self.keepGoing = True
        self.view = view
        self.squares = [model.Square(100, (350, 150), GREEN),
                        model.Square(100, (500, 150), RED),
                        model.Square(100, (350, 260), YELLOW),
                        model.Square(100, (500, 260), BLUE)]

    def run(self):
        clock = pygame.time.Clock()
        while self.keepGoing:
            clock.tick(60)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.keepGoing = False

            event_pos = self.get_event(events)
            self.handle_events(event_pos)
            self.init_window()

    def init_window(self):
        self.view.show_window(self.squares)

    def get_event(self, ev):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                return pygame.mouse.get_pos()

        return None

    def handle_events(self, pos):
        if pos:
            for square in self.squares:
                rect = self.view.get_rect_from_square(square)
                if rect.collidepoint(pos):
                    original_color = square.color
                    new_color = (
                        original_color[0] + (255 - original_color[0]) * 1 / 4,
                        original_color[1] + (255 - original_color[1]) * 1 / 2,
                        original_color[2] + (255 - original_color[2]) * 3 / 4,)
                    square.update_color(new_color)
                    timer = Timer(0.5, lambda: square.update_color(original_color))
                    timer.start()
                    return
