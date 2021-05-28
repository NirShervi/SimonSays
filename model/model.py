import random


class Square:
    """ This class represent a Rectangle we show on the screen
    :param height,position,color
    :return:
    """

    def __init__(self, height, position, color, width=None):
        self.height = height
        self.width = width
        self.position = position
        self.color = color
        self.main_color = color
        self.secondary_color = (
            color[0] + (255 - color[0]) * 1 / 4,
            color[1] + (255 - color[1]) * 1 / 2,
            color[2] + (255 - color[2]) * 3 / 4,)

        if width is None:
            self.width = height

    def update_color(self, color):
        """ update the color of the Rectangle
        :param color: Tuple that represent RGB color
        :return:
        """
        self.color = color


class Button(Square):
    """ This class represent a Button
    :param
    :return:
    """

    def __init__(self, height, position, color, sound_path="", text=None, on_click=None, width=None):
        super().__init__(height, position, color, width)
        self.sound_path = sound_path
        self.text = text
        self.on_click = on_click
        self.text_positionX = self.position[0] + 45
        self.text_positionY = self.position[1] + 10


class Simon:
    """ This class represent Simon, Simon is responsible to show the steps and set the lvl
    :param
    :return:
    """

    def __init__(self):
        self.challenge = []
        self.steps_to_show = []
        self.lvl = 1

    def init_challenge(self):
        self.challenge = []
        self.steps_to_show = []
        for x in range(self.lvl):
            num = random.randint(0, 3)
            self.challenge.append(num)
            self.steps_to_show.append(num)


class Player:
    """ This class represent Player, Player needs to flow simon steps, and also this class saves the player name and
    tracking the player score.
    :param
    :return:
    """

    def __init__(self, player_name, all_scores):
        self.score = 0
        self.steps_done = []
        self.total_score = 0
        self.name = player_name
        for name, score in all_scores:
            if name == self.name:
                self.total_score = score


class Text:
    """ This class represent Text we want to show on the screen.
      :param small: if we want the font to be small
      :return:
      """

    def __init__(self, txt, x, y, small=False):
        self.msg = txt
        self.x = x
        self.y = y
        self.small = small
