import time
from model import model
from colors import *
from threading import Timer
from db import *


class Controller:
    """ This class represent the main controller, the main controller is responsible to switch between different controllers
      :param view: the main view class,
      :param rows: a list of tuple that represent the score table,
      :param conn: a a connection to the database
      :return:
      """

    def __init__(self, view, rows, conn):
        self.current_player = model.Text("", 405, 125)
        self.players_and_scores = rows
        self.game_controller = GameController(view, self.current_player, self.players_and_scores, conn)
        self.main_controller = MainMenuController(view, self.current_player, self.players_and_scores, conn)
        self.mode = MAIN_MOD
        self.view = view
        self.db_conn = conn

    def run(self):
        """ This function responsible to get the events and pass them to the controllers.
        Each iteration of the while loop in this function is a frame.
          :param
          :return:
          """
        clock = pygame.time.Clock()
        while self.mode is not EXIT:
            clock.tick(60)

            events = pygame.event.get()
            if self.mode == PLAY_MOD:
                mode_tmp = self.game_controller.run(events)
            else:
                mode_tmp = self.main_controller.run(events)
            if mode_tmp != self.mode:
                if mode_tmp == MAIN_MOD:
                    self.players_and_scores = self.game_controller.players_and_scores
                self.mode = mode_tmp
                self.game_controller = GameController(self.view, self.current_player, self.players_and_scores,
                                                      self.db_conn)
                self.main_controller = MainMenuController(self.view, self.current_player, self.players_and_scores,
                                                          self.db_conn)

                self.view.update_view()


class AbstractController:
    """ This class is an abstract class. Do not use it by itself! The MainController and GameController inherit this
    class. The controller is responsible to decide what to show on the screen and on which object we can click

      :param
      :return:
      """

    def __init__(self, view, player_name, players_and_scores, conn):
        self.view = view
        self.players_and_scores = players_and_scores
        self.current_player = player_name
        self.to_display = []
        self.main_text = None
        self.sleep = False
        self.keepGoing = True
        self.db_conn = conn

    def init_window(self):
        """ Init window is responsible to show the object that are inside to_display list
          :param
          :return:
          """
        self.view.show_window(self.to_display)

    def update_main_txt(self, new_txt):
        """ update_main_txt updating the main_text object
          :param new_txt: the new text we want to show on the screen
          :return:
          """
        self.view.update_view()
        self.main_text.msg = new_txt
        if self.main_text not in self.to_display:
            self.to_display.append(self.main_text)
        self.sleep = True


class GameController(AbstractController):
    """ The game controller is the controller that handle all the events in the play screen, and decides what to show on
    the screen.
      :param
      :return:
      """

    def __init__(self, view, player_name, players_and_scores, conn):
        super().__init__(view, player_name, players_and_scores, conn)
        self.simon = model.Simon()
        self.player = model.Player(player_name.msg, players_and_scores)
        self.keepGoing = PLAY_MOD
        self.squares = [
            model.Button(100, (350, 150), GREEN, "./sounds/beep1.ogg", on_click=self.handle_square_event(0)),
            model.Button(100, (500, 150), RED, "./sounds/beep2.ogg", on_click=self.handle_square_event(1)),
            model.Button(100, (350, 260), YELLOW, "./sounds/beep3.ogg", on_click=self.handle_square_event(2)),
            model.Button(100, (500, 260), BLUE, "./sounds/beep4.ogg", on_click=self.handle_square_event(3))]
        self.start_button = model.Button(50, (400, 50), ORANGE, text="Start", width=150,
                                         on_click=self.handle_start_event())
        self.restart_button = model.Button(50, (10, 80), GREEN, on_click=self.restart, text="Try again",
                                           width=200)
        self.back_button = model.Button(50, (10, 150), ORANGE, on_click=self.handle_back_event, text="Main menu",
                                        width=200)
        self.redo_txt = model.Text("Click the bottom bellow to return to the prev stage", 360, 370, True)
        self.redo_button = model.Button(50, (360, 400), ORANGE, on_click=self.handle_prev_lvl, text="Previous level",
                                        width=200)
        self.score_txt = model.Text("Score : 0", 10, 10)
        self.simon_turn = False
        self.main_text = model.Text("Simon's Turn", 400, 50)
        self.originator = model.Originator()
        self.states = []
        self.to_display = [*self.squares, self.start_button, self.score_txt]
        self.clickable = [*self.squares, self.start_button]
        self.blinks = 0
        self.sleep_time = 1
        self.sleep = False
        self.game_started = False

    def restart(self):
        """ Reset the GameController object to the initial value
          :param
          :return:
          """
        self.view.update_view()
        self.__init__(self.view, self.current_player, self.players_and_scores, self.db_conn)

    def run(self, events):
        """ Runs the game, each call of this function is a frame
          :param events: a list of pygame events
          :return: the next mod we want to be
          """
        for event in events:
            if event.type == pygame.QUIT:
                self.keepGoing = EXIT
            elif event.type == SHOW_SIMON_TURN:
                if event.show_turn == "True":
                    self.show_simon_turn()
                else:
                    self.sleep = True
                    self.show_steps()
            elif event.type == YOUR_TURN:
                self.sleep = False
                self.show_player_turn()

        event_pos = get_event(events)
        self.handle_events(event_pos)
        self.check_turn()
        self.init_window()
        if self.sleep:
            time.sleep(self.sleep_time)
            self.sleep_time = 1
            self.sleep = False

        return self.keepGoing

    def handle_events(self, pos):
        """ handle events handle user events or pygame events
          :param pos: if user clicked on the screen, pos represent the click position
          :return:
          """
        if pos:
            for square in self.clickable:
                rect = self.view.get_rect_from_square(square)
                if rect.collidepoint(pos):
                    if not self.simon_turn:
                        square.on_click()
                    elif square == self.restart_button:
                        square.on_click()
                    elif square == self.back_button:
                        square.on_click()
                    elif square == self.redo_button:
                        square.on_click()
                    return

    def handle_square_event(self, i):
        """
          :param i: index of a button in our squares list
          :return: a function to be called when a user clicked on a square
          """
        return lambda: self.handle_player_move(i)

    def handle_start_event(self):
        """ This function block user click event.
          :param
          :return a function to be called when a user click on an event:
          """
        return self.show_simon_turn

    def handle_back_event(self):
        """ This function set the next mod to be the main mod. after calling this function we will be in the main menu
          :param
          :return:
          """
        self.keepGoing = MAIN_MOD

    def handle_player_move(self, index):
        """ This function check if user was right when he making a step, also this function responsible to
        make the squares blink and to let the user know if he was wrong
          :param index: index represent the index of a square in our squares list
          :return:
          """
        if self.game_started:
            if self.simon.challenge[len(self.player.steps_done)] == index:
                self.blink(index, False)
                self.player.steps_done.append(index)
            else:
                super().update_main_txt("Oh no! Wrong answer :( ")
                self.simon_turn = True
                self.to_display.append(self.restart_button)
                self.clickable.append(self.restart_button)
                self.to_display.append(self.back_button)
                self.clickable.append(self.back_button)
                if self.simon.lvl > 1:
                    self.to_display.append(self.redo_button)
                    self.clickable.append(self.redo_button)
                    self.to_display.append(self.redo_txt)
                insert_row(self.db_conn, (self.player.name, self.player.total_score))
                self.players_and_scores = get_all_rows(self.db_conn)

    def show_simon_turn(self, custom_lvl=None):
        """ Letting the user know that is now Simon turn's
          :param
          :return:
          """
        self.simon_turn = True
        self.game_started = True
        self.view.update_view()
        self.simon.init_challenge(custom_lvl)
        self.originator.set(self.simon.challenge[:])
        self.states.append(self.originator.save_to_memento())
        if self.start_button in self.to_display:
            self.to_display.remove(self.start_button)
            self.clickable.remove(self.start_button)

        super().update_main_txt("Simon's Turn")
        pygame.event.post(SIMON_TURN_EVENT)

    def handle_prev_lvl(self):
        self.to_display.remove(self.restart_button)
        self.clickable.remove(self.restart_button)
        self.to_display.remove(self.back_button)
        self.clickable.remove(self.back_button)
        self.to_display.remove(self.redo_button)
        self.to_display.remove(self.redo_txt)
        self.originator.restore_from_memento(self.states[-2])
        prev_lvl = self.originator.save_to_memento().get_saved_state()
        self.states.pop()
        self.show_simon_turn(custom_lvl=prev_lvl)

    def show_player_turn(self):
        """Letting the user know that now is the user turn
          :param
          :return:
          """
        self.view.update_view()
        super().update_main_txt("Your Turn")

    def show_steps(self):
        """ Showing the user the steps he needs to follow
          :param
          :return:
          """
        if len(self.simon.steps_to_show) > 0:
            index = self.simon.steps_to_show.pop(0)
            self.blink(index, True)
        if len(self.simon.steps_to_show) > 0:
            pygame.event.post(SIMON_TURN_EVENT)

    def blink(self, index, update_blinks):
        """ Making a square blink and also make a sound
          :param index: represent a index in the squares list.
          :param update_blinks: if we want to count this as a simon step or user step
          :return:
          """
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
        """ Checks if this is the user turn or simon turn
          :param
          :return:
          """
        if self.blinks == self.simon.lvl:
            self.blinks = 0
            self.simon_turn = False
            pygame.event.post(YOUR_TURN_EVENT)
        elif len(self.player.steps_done) == self.simon.lvl:
            self.player.steps_done = []
            super().update_main_txt("Good Job!")
            self.simon.lvl += 1
            self.player.score += 10
            self.player.total_score += 10
            self.score_txt.msg = f"Score: {self.player.score}"
            event = pygame.event.Event(SHOW_SIMON_TURN, show_turn="True")
            timer = Timer(1, lambda: pygame.event.post(event))
            timer.start()


class MainMenuController(AbstractController):
    """ This is the controller that responsible to handle the events in the main menu and decides what to show on the
    screen
      :param
      :return:
      """

    def __init__(self, view, player_name, players_and_scores, conn):
        super().__init__(view, player_name, players_and_scores, conn)
        self.main_text = model.Text("Welcome to Simon!", 350, 50)
        self.enter_your_name = model.Text("Please enter your name bellow:", 400, 90, small=True)
        self.play_button = model.Button(50, (400, 200), ORANGE, on_click=self.change_mod,
                                        text="Play", width=150)
        self.input_box = model.Button(50, (400, 120), PASSIVE_INPUT, width=150, on_click=self.handle_input_active)
        self.top_players = model.Text("Top 5 players:", 400, 250)
        self.input_active = False
        self.to_display = [self.main_text, self.play_button, self.input_box, self.enter_your_name, self.top_players]
        self.clickable = [self.play_button, self.input_box]
        self.keepGoing = MAIN_MOD
        self.draw_top_players()

    def run(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.keepGoing = EXIT
            if event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_BACKSPACE:
                    self.current_player.msg = self.current_player.msg[:-1]
                    self.input_box.text = self.current_player.msg.strip()
                    self.view.update_view()
                else:
                    self.current_player.msg += event.unicode
                    self.input_box.text = self.current_player.msg.strip()
                    self.view.update_view()

        event_pos = get_event(events)
        self.handle_events(event_pos)
        if self.input_active:
            self.input_box.color = ACTIVE_INPUT
        else:
            self.input_box.color = PASSIVE_INPUT

        self.init_window()
        return self.keepGoing

    def change_mod(self):
        tmp_name = self.current_player.msg.replace(" ", "")
        if tmp_name != "":
            self.keepGoing = PLAY_MOD

    def handle_events(self, pos):
        if pos:
            for square in self.clickable:
                rect = self.view.get_rect_from_square(square)
                if rect.collidepoint(pos):
                    square.on_click()
                else:
                    self.input_active = False

    def handle_input_active(self):
        self.input_active = True

    def draw_top_players(self):
        """ This function draw the top players table
          :param
          :return:
          """
        index = 1
        for name, score in self.players_and_scores:
            tmp_txt = model.Text(f"{index}) {name} : {score}", 400, 300 + (index - 1) * 40)
            self.to_display.append(tmp_txt)
            index += 1


def get_event(ev):
    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP:
            return pygame.mouse.get_pos()
