class Square:
    def __init__(self, size, position, color,sound_path):
        self.size = size
        self.position = position
        self.color = color
        self.main_color = color
        self.secondary_color = (
            color[0] + (255 - color[0]) * 1 / 4,
            color[1] + (255 - color[1]) * 1 / 2,
            color[2] + (255 - color[2]) * 3 / 4,)
        self.sound_path = sound_path

    def update_color(self, color):
        self.color = color
