import math

import pygame

from alien import Alien


class Heart(Alien, pygame.sprite.Sprite):
    # A class to model a love heart which will give the player an extra life

    def __init__(self, x, y, velocity, heart_group, heart_bullet_group, width, height):
        super().__init__(x, y, velocity, heart_group, heart_bullet_group, width, height)
        self.image = pygame.image.load("images/Love_Heart.png")
        heart_size = (100, 100)  # resizing the heart
        self.image = pygame.transform.scale(self.image, heart_size)
        self.rect = self.image.get_rect()
        self.rect.x = width - 100  # Initial x position
        self.rect.y = 75  # Initial y position
        self.time = 0  # Initialize time to control oscillation
        self.amplitude = 75  # Oscillation amplitude (height of the sine wave)
        self.frequency = 0.05  # Oscillation frequency (controls speed of the sine wave)
        self.width = width
        self.height = height
        self.starting_x = x  # This aims to make resetting the aliens alot easier.
        self.starting_y = y
        self.velocity = 1  # choosing to be very kind and making the heart speed consistent even when the rounds progress.
        self.heart_group = heart_group
        self.heart_bullet_group = heart_bullet_group

    def update(self):
        self.oscillate()

    def oscillate(self):
        # Update the x position using a sine wave for oscillation
        self.rect.x -= self.velocity  # move at a different rate compared to the aliens
        self.rect.y = 200 + self.amplitude * math.sin(self.time)
        self.time += self.frequency  # Increment time to create oscillation
