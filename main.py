import pygame

from game import Game
from player import Player

# Initialise pygame
pygame.init()

# Set display surface
WIDTH = 1200
HEIGHT = 900
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Set frames per second and clock
FPS = 60
clock = pygame.time.Clock()
BOOST_TIME_IN_SECS = 4

# Create bullet groups
my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group()
my_chest_bullet_group = pygame.sprite.Group()
my_heart_bullet_group = pygame.sprite.Group()

# Create a player group and player object
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group, WIDTH, HEIGHT, FPS,
                   BOOST_TIME_IN_SECS)  # so that the player class has access to the bullet class.
my_player_group.add(my_player)

# Create an alien group. Will add Alien objects via the game's start new round method.
my_alien_group = pygame.sprite.Group()

# Create a chest group. Will add Chest objects via the game's start new round method.
my_chest_group = pygame.sprite.Group()

# Create a love heart group
my_heart_group = pygame.sprite.Group()

# Create a game object
my_game = Game(my_player, my_player_group, my_alien_group, my_chest_group, my_heart_group, my_player_bullet_group,
               my_alien_bullet_group, my_chest_bullet_group, my_heart_bullet_group, WIDTH, HEIGHT, FPS, display_surface)
my_game.start_new_round()

start_time = pygame.time.get_ticks()  # Outside the game loop

# The main game loop
while my_game.running:
    # Check to see if the user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            my_game.running = False

        # The player wants to fire
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.fire()

    # Fill the display
    display_surface.fill((236, 198, 230))

    # Update and display all sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_alien_group.update()
    my_alien_group.draw(display_surface)

    my_chest_group.update()
    my_chest_group.draw(display_surface)

    cycle_duration = 5000  # 5 seconds on or off, hard to get this value quite right
    current_time = pygame.time.get_ticks()  # this gets the current time
    time_passed = (current_time - start_time) % cycle_duration  # this creates a repeated cycle of 10 seconds
    if time_passed < cycle_duration / 2:  # if we are in the first half of the cycle, draw and update the love heart
        my_heart_group.draw(display_surface)
        my_heart_group.update()

    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(display_surface)

    my_chest_bullet_group.update()
    my_chest_bullet_group.draw(display_surface)

    my_heart_bullet_group.update()
    my_heart_bullet_group.draw(display_surface)

    # Update and draw object
    my_game.update()
    my_game.draw()

    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
