import pygame
from model import model
from colors import *
from threading import Timer


class Controller:

    def __init__(self, view):
        self.keepGoing = True
        self.view = view
        self.squares = [model.Square(100, (350, 150), GREEN, "./sounds/beep1.ogg"),
                        model.Square(100, (500, 150), RED, "./sounds/beep2.ogg"),
                        model.Square(100, (350, 260), YELLOW, "./sounds/beep3.ogg"),
                        model.Square(100, (500, 260), BLUE, "./sounds/beep4.ogg")]

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
                    square.update_color(square.secondary_color)
                    pygame.mixer.music.load(square.sound_path)
                    pygame.mixer.music.play(0)
                    timer = Timer(0.3, lambda: square.update_color(square.main_color))
                    timer.start()
                    return
