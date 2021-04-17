import pygame


class Square:
    def __init__(self, size, position, color):
        self.size = size
        self.position = position
        self.color = color

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size, self.size)

    def update_color(self, color):
        self.color = color
