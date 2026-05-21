import pygame
import random
from gameoflife import config
from gameoflife.app import App
from gameoflife.grid import GridData, GridGeometry
from gameoflife.math_utils import point_in_rect
from gameoflife.settings import AppSettings

def main():
    app = App.create()
    app.run()

if __name__ == "__main__":
    main()
