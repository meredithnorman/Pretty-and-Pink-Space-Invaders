from random import randint

import pygame

from alienBullet import AlienBullet


class Alien(pygame.sprite.Sprite):  # use the sprite.Sprite as you have to inherit from the game class
    # A class to model an enemy alien

    def __init__(self, x, y, velocity, alien_group, alien_bullet_group, width, height):
        # Initialise the alien
        super().__init__()
        self.image = pygame.image.load("images/purple_invader.svg")
        alien_size = (87, 87)  # resizing the ship
        self.image = pygame.transform.scale(self.image, alien_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.starting_x = x  # This aims to make resetting the aliens alot easier.
        self.starting_y = y
        self.width = width
        self.height = height
        self.direction = 1  # Positive 1 is moving to the right, -1 is moving to the left.
        self.velocity = velocity
        self.alien_group = alien_group
        self.alien_bullet_group = alien_bullet_group
        self.shoot_sound = pygame.mixer.Sound("sounds/alien_fire.wav")

    def update(self):
        # update the alien
        self.rect.x += self.direction * self.velocity  # ie left or right and then velocity

        # Randomly fire a bullet
        if randint(0, 3000) > 2995 + 0.06 * len(self.alien_group) and len(self.alien_bullet_group) < 3:
            # When there are fewer aliens, the probability of shooting increases slightly. This probably isn't the most optimal way of doing it. I also make sure there are max 3 bullets at once fron the aliens.
            self.fire()

    def fire(self):
        # Fire a bullet
        AlienBullet(self.rect.centerx, self.rect.bottom, self.alien_bullet_group, self.width, self.height)

    def reset(self):
        # Reset the aliens position
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.direction = 1
