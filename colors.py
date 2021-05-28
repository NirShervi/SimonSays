import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BRIGHTRED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BRIGHTYELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BRIGHTBLUE = (0, 0, 255)
GREEN = (50, 205, 50)
BRIGHTGREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PASSIVE_INPUT = pygame.Color('chartreuse4')
ACTIVE_INPUT = pygame.Color('lightskyblue3')

SHOW_SIMON_TURN = pygame.USEREVENT + 1
SIMON_TURN_EVENT = pygame.event.Event(SHOW_SIMON_TURN, show_turn="False")
YOUR_TURN = pygame.USEREVENT + 2
YOUR_TURN_EVENT = pygame.event.Event(YOUR_TURN)

EXIT = -1
PLAY_MOD = 1
MAIN_MOD = 2
