import random

class Particle:
    def __init__(self, x : float = 0, y : float = 0):
        self.x = x
        self.y = y
        self.vx = None
        self.vy = None

    def print(self):
        print(f'x: {self.x}, y: {self.y}')