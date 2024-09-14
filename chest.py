import pygame

from alien import Alien


class Chest(Alien):
    # A class to model a treasure chest

    def __init__(self, x, y, velocity, chest_group, chest_bullet_group, width, height):
        super().__init__(x, y, velocity, chest_group, chest_bullet_group, width, height)
        self.image = pygame.image.load("images/treasure_chest.png")
        chest_size = (50, 50)  # resizing the ship
        self.image = pygame.transform.scale(self.image, chest_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.starting_x = x  # This aims to make resetting the aliens alot easier.
        self.starting_y = y
        self.direction = 1  # Positive 1 is moving to the right, -1 is moving to the left.
        self.velocity = velocity
        self.width = width
        self.height = height
        self.chest_group = chest_group
        self.chest_bullet_group = chest_bullet_group
        self.shoot_sound = pygame.mixer.Sound("sounds/alien_fire.wav")

    def fire(self):
        pass
