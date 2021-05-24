import pygame
import time
from model import model
from colors import *
from threading import Timer

SHOW_SIMON_TURN = pygame.USEREVENT + 1
SIMON_TURN_EVENT = pygame.event.Event(SHOW_SIMON_TURN)
YOUR_TURN = pygame.USEREVENT + 2
YOUR_TURN_EVENT = pygame.event.Event(YOUR_TURN)


class Controller:

    def __init__(self, view):
        self.simon = model.Simon()
        self.player = model.Player()

        self.keepGoing = True
        self.view = view
        self.squares = [
            model.Button(100, (350, 150), GREEN, "./sounds/beep1.ogg", on_click=self.handle_square_event(0)),
            model.Button(100, (500, 150), RED, "./sounds/beep2.ogg", on_click=self.handle_square_event(1)),
            model.Button(100, (350, 260), YELLOW, "./sounds/beep3.ogg", on_click=self.handle_square_event(2)),
            model.Button(100, (500, 260), BLUE, "./sounds/beep4.ogg", on_click=self.handle_square_event(3))]
        self.start_button = model.Button(50, (400, 50), ORANGE, text="Start", width=150,
                                         on_click=self.handle_start_event())
        self.score_txt = model.Text("Score : 0", 10, 10)
        self.simon_turn = False
        self.simon_turn_txt = model.Text("Simon's Turn", 400, 50)
        self.your_turn_txt = model.Text("Your Turn", 400, 50)
        self.to_display = [*self.squares, self.start_button, self.score_txt]
        self.clickable = [*self.squares, self.start_button]
        self.blinks = 0
        self.sleep = False

    def run(self):
        clock = pygame.time.Clock()
        while self.keepGoing:
            clock.tick(60)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.keepGoing = False
                elif event.type == SHOW_SIMON_TURN:
                    self.sleep = True
                    self.show_steps()
                elif event.type == YOUR_TURN:
                    self.show_player_turn()

            event_pos = self.get_event(events)

            self.handle_events(event_pos)
            self.check_turn()
            self.init_window()
            if self.sleep:
                time.sleep(1)
                self.sleep = False

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
                    if not self.simon_turn:
                        square.on_click()
                    return

    def handle_square_event(self, i):
        return lambda: self.handle_player_move(i)

    def handle_start_event(self):
        self.simon_turn = True
        return self.show_simon_turn

    def handle_player_move(self, index):
        if len(self.player.steps_done) == 0:
            if self.simon.challenge[0] == index:
                self.blink(index, False)
                self.player.steps_done.append(index)
            else:
                pass
        else:
            if self.simon.challenge[len(self.player.steps_done)] == index:
                self.blink(index, False)
                self.player.steps_done.append(index)
            else:
                pass

    def show_simon_turn(self):
        self.view.update_view()
        self.simon.init_challenge()
        if self.start_button in self.to_display:
            self.to_display.remove(self.start_button)
            self.clickable.remove(self.start_button)
        if self.your_turn_txt in self.to_display:
            self.to_display.remove(self.your_turn_txt)
        self.to_display.append(self.simon_turn_txt)
        pygame.event.post(SIMON_TURN_EVENT)

    def show_player_turn(self):
        self.view.update_view()
        self.to_display.remove(self.simon_turn_txt)
        self.to_display.append(self.your_turn_txt)

    def show_steps(self):
        if len(self.simon.steps_to_show) > 0:
            index = self.simon.steps_to_show.pop()
            self.blink(index, True)
        if len(self.simon.steps_to_show) > 0:
            pygame.event.post(SIMON_TURN_EVENT)

    def blink(self, index, update_blinks):
        square = self.squares[index]
        square.update_color(square.secondary_color)
        pygame.mixer.music.load(square.sound_path)
        pygame.mixer.music.play(0)

        def change_color_back():
            square.update_color(square.main_color)
            if update_blinks:
                self.blinks += 1

        timer = Timer(0.3, change_color_back)
        timer.start()

    def check_turn(self):
        if self.blinks == self.simon.lvl:
            self.blinks = 0
            self.simon_turn = False
            pygame.event.post(YOUR_TURN_EVENT)
        elif len(self.player.steps_done) == self.simon.lvl:
            self.player.steps_done = []
            timer = Timer(1, self.show_simon_turn)
            timer.start()
