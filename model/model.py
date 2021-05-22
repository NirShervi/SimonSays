import random


class Square:
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
        self.color = color


class Button(Square):
    def __init__(self, height, position, color, sound_path="", text=None, on_click=None, width=None):
        super().__init__(height, position, color, width)
        self.sound_path = sound_path
        self.text = text
        self.on_click = on_click
        self.text_positionX = self.position[0] + 45
        self.text_positionY = self.position[1] + 10


class Simon:
    def __init__(self):
        self.challenge = []
        self.lvl = 3

    def init_challenge(self):
        self.challenge = []
        for x in range(self.lvl):
            self.challenge.append(random.randint(0, 3))


class Text:
    def __init__(self, txt, x, y):
        self.msg = txt
        self.x = x
        self.y = y
