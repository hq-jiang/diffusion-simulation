import random
import numpy as np
from typing import List
import cv2

from particle import Particle

class DiffusionManager:
    def __init__(self, bottom_x, top_x, bottom_y, top_y):

        # Particle borders
        self.bottom_x = bottom_x
        self.top_x = top_x
        self.bottom_y = bottom_y
        self.top_y = top_y

        # Virtual border
        self.border = (bottom_x + top_x) // 2

        # Particles
        self.particles = None

    def init_particles(self, n_left, n_right):
        self.particles = [Particle() for i in range(n_left + n_right)]
        self.set_rand_position(n_left, n_right)

    def set_rand_position(self, n_left, n_right):
        
        for i in range(n_left):
            self.particles[i].x = random.random() * (self.border - self.bottom_x) + self.bottom_x
            self.particles[i].y = random.random() * (self.top_y - self.bottom_y) + self.bottom_y

        for i in range(n_left, n_left + n_right):

            self.particles[i].x = random.random() * (self.top_x - self.border) + self.border
            self.particles[i].y = random.random() * (self.top_y - self.bottom_y) + self.bottom_y

    def move_particles(self, k):
        for particle in self.particles:
            rand_x = random.random() * 2 - 1
            rand_y = random.random() * 2 - 1

            delta_x = rand_x * k
            delta_y = rand_y * k

            if delta_x + particle.x < self.top_x and delta_x + particle.x > self.bottom_x:
                particle.x += delta_x
            else: 
                particle.x -= delta_x
            if delta_y + particle.y < self.top_y and delta_y + particle.y > self.bottom_y:
                particle.y += delta_y
            else:
                particle.y -= delta_y

    def calc_concentration(self):
        left_concentration = 0
        right_concentration = 0
        for particle in self.particles:
            if particle.x < self.border:
                left_concentration += 1
            else:
                right_concentration += 1
        return left_concentration, right_concentration


class ParticleDrawer:
    def __init__(self, bottom_x, top_x, bottom_y, top_y, border):
        self.bottom_x = bottom_x
        self.top_x = top_x
        self.bottom_y = bottom_y
        self.top_y = top_y
        self.border = border

        self.line_width = 1
        
        self.img_width = top_x + bottom_x
        self.img_height = top_y + bottom_y
        
        self.img = np.zeros((self.img_height, self.img_width, 3), np.uint8) 
        
    def draw(self, particles : List[Particle], left_concentration, right_concentration, n_left=None):
        self.img *= 0

        # Draw white container space
        self.img = cv2.rectangle(self.img, 
                                (self.bottom_x - 1, self.bottom_y - 1), 
                                (self.top_x + 1, self.top_y + 1), 
                                (255,255,255), 
                                -1)
        # Draw border line
        self.img = cv2.line(self.img, (self.border, self.bottom_y), (self.border, self.top_y), (128, 128, 128), 1)
        if n_left is None:
            for particle in particles:
                cv2.circle(self.img, (int(particle.x), int(particle.y)), self.line_width, (0,0,255), -1)
        else:
            for i in range(n_left):
                cv2.circle(self.img, (int(particles[i].x), int(particles[i].y)), self.line_width, (0,0,255), -1)
            for i in range(n_left, len(particles)):
                cv2.circle(self.img, (int(particles[i].x), int(particles[i].y)), self.line_width, (255,0,0), -1)

        # Draw concentration text
        position_left = (self.bottom_x, self.top_y + self.bottom_y - 15)
        position_right = (self.border, self.top_y + self.bottom_y - 15)
        self.img = cv2.putText(self.img, str(left_concentration), position_left, cv2.FONT_HERSHEY_SIMPLEX, 
                          1, (255, 255, 255), 2, cv2.LINE_AA) 
        self.img = cv2.putText(self.img, str(right_concentration), position_right, cv2.FONT_HERSHEY_SIMPLEX, 
                          1, (255, 255, 255), 2, cv2.LINE_AA) 
        cv2.imshow('diffusion', self.img)
        