import pygame

from playerBullet import PlayerBullet


class Player(pygame.sprite.Sprite):  # use the sprite.Sprite as you have to inherit from the game class
    # A class to model a spaceship the user can control

    def __init__(self, bullet_group, width, height, fps, boost_time_in_secs):
        # Initialise the player
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.image.load("images/Ship.png")
        ship_size = (100, 100)  # resizing the ship
        self.image = pygame.transform.scale(self.image, ship_size)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height  # so positioning the ship in the center at the bottom of the screen.
        self.lives = 5
        self.velocity = 8
        self.bullet_group = bullet_group
        self.boost = False
        self.fps = fps
        self.boost_time_in_secs = boost_time_in_secs
        self.boost_timer = fps * self.boost_time_in_secs
        self.shoot_sound_boost = pygame.mixer.Sound("sounds/laser_fire.mp3")
        self.shoot_sound_normal = pygame.mixer.Sound("sounds/player_fire.wav")
        self.accuracy = 0.0
        self.hits = 0
        self.attempts = 0

    def update(self):
        # update the player
        keys = pygame.key.get_pressed()

        # move the player within the bounds of the screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < self.width:
            self.rect.x += self.velocity

        if self.boost:
            self.boost_timer -= 1
        if self.boost_timer == 0:
            self.boost = False
            self.boost_timer = self.fps * self.boost_time_in_secs

    def fire(self):
        self.attempts += 1
        self.update_accuracy()
        # Fire a bullet
        if self.boost:
            self.shoot_sound_boost.play()
        else:
            self.shoot_sound_normal.play()
        PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group,
                     self.boost)  # fire from the top of the ship. We are using the Player Bullet class and have to put in all the neccessary inputs.

    def update_accuracy(self):  # Making a function seemed like the easiest way to calculate and update accuracy
        if self.attempts > 0:
            self.accuracy = round((self.hits / self.attempts) * 100, 1)
        else:
            self.accuracy = 0  # make sure that you don't just get//0

    def reset(self):
        # Reset the players position
        self.rect.centerx = self.width // 2
        self.boost = False
        self.boost_timer = self.fps * self.boost_time_in_secs
