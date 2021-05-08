import pygame
from model import model
from colors import *
from threading import Timer


class Controller:

    def __init__(self, view):
        self.keepGoing = True
        self.view = view
        self.squares = [model.Button(100, (350, 150), GREEN, "./sounds/beep1.ogg", on_click=handle_square_event),
                        model.Button(100, (500, 150), RED, "./sounds/beep2.ogg", on_click=handle_square_event),
                        model.Button(100, (350, 260), YELLOW, "./sounds/beep3.ogg", on_click=handle_square_event),
                        model.Button(100, (500, 260), BLUE, "./sounds/beep4.ogg", on_click=handle_square_event)]
        self.start_button = model.Button(50, (400, 50), ORANGE, text="Start", width=150)
        self.to_display = [*self.squares, self.start_button]
        self.clickable = [*self.squares, self.start_button]

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
        self.view.show_window(self.to_display)

    def get_event(self, ev):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                return pygame.mouse.get_pos()

        return None

    def handle_events(self, pos):
        if pos:
            for square in self.clickable:
                rect = self.view.get_rect_from_square(square)
                if rect.collidepoint(pos):
                    square.on_click(square)
                    return


def handle_square_event(square):
    square.update_color(square.secondary_color)
    pygame.mixer.music.load(square.sound_path)
    pygame.mixer.music.play(0)
    timer = Timer(0.3, lambda: square.update_color(square.main_color))
    timer.start()
