from vec import vec
import pygame
from circle import Ball, Player

class Box:
    def __init__(self, width: float, height: float, window_width: float, window_height: float) -> None:
        self.width = width
        self.height = height
        self.position = vec((window_width - width) / 2, (window_height - height) / 2)  # Center position

    def render(self, window) -> None:
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect(self.position.x, self.position.y, self.width, self.height), 2)
