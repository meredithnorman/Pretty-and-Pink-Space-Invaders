import pygame


class AlienBullet(pygame.sprite.Sprite):
    # A class to model a bullet fired by the alien

    def __init__(self, x, y, bullet_group, width, height):
        # Initialise the bullet
        super().__init__()
        self.image = pygame.image.load("images/red_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.width = width
        self.height = height
        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        # update the bullet
        self.rect.y += self.velocity

        # If the bullet is off the screen, remove it.
        if self.rect.top > self.height:
            self.kill()  # kill is dramatic
    # Note we are checking for collisions inside our game object so we don't need to here.
