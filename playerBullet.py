import pygame


class PlayerBullet(pygame.sprite.Sprite):
    # A class to model a bullet fired by the player

    def __init__(self, x, y, bullet_group,
                 boost):  # The bullet group aims to minimise the number of bullets on the screen at any given time.
        # Initialise the bullet
        super().__init__()
        self.boost = boost
        if self.boost:
            self.image = pygame.image.load("images/boost_laser.png")
        else:
            self.image = pygame.image.load("images/green_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        # update the bullet
        if self.boost:
            self.rect.y = self.rect.y - (self.velocity * 3)
        else:
            self.rect.y -= self.velocity

        # If the bullet is off the screen, remove it.
        if self.rect.bottom < 0:
            self.kill()  # kill is dramatic

    # Note we are checking for collisions inside our game object so we don't need to here.
