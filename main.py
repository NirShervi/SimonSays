import pygame
from view import View
from controller import Controller


def main():
    view = View.View()
    controller = Controller.Controller(view)
    controller.run()


if __name__ == "__main__":
    main()
