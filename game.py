from random import randint

import pygame

from alien import Alien
from chest import Chest
from heart import Heart


class Game:
    # A class to help control and update gameplay

    def __init__(self, player, player_group, alien_group, chest_group, heart_group, player_bullet_group,
                 alien_bullet_group, chest_bullet_group, heart_bullet_group, width, height, fps, display_surface):
        # initialise the game
        # Set game values
        self.round_number = 1
        self.score = 0
        self.player = player
        self.player_group = player_group
        self.alien_group = alien_group
        self.chest_group = chest_group
        self.heart_group = heart_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group
        self.chest_bullet_group = chest_bullet_group
        self.heart_bullet_group = heart_bullet_group
        self.width = width
        self.height = height
        self.fps = fps
        self.display_surface = display_surface
        self.running = True

        # Set sounds and music
        self.new_round_sound = pygame.mixer.Sound("sounds/new_round.wav")
        self.breach_sound = pygame.mixer.Sound("sounds/breach.wav")  # i.e. the aliens 'breach' the bounds of the screen
        self.player_hit_sound = pygame.mixer.Sound("sounds/player_hit.wav")
        self.alien_hit_sound = pygame.mixer.Sound("sounds/alien_hit.wav")
        self.chest_hit_sound = pygame.mixer.Sound("sounds/bonus_acquired.wav")
        self.heart_hit_sound = pygame.mixer.Sound("sounds/heart_wav.wav")

        # Set font
        self.font = pygame.font.SysFont('candara', 32, bold=10)

    def update(self):
        # update the game
        self.shift_aliens()
        self.check_collisions()
        self.check_round_completion()

    def draw(self):
        # Draw information to the display
        white = (255, 255, 255)

        # Set text
        score_text = self.font.render("SCORE: " + str(self.score), True, white)
        score_rect = score_text.get_rect()
        score_rect.centerx = self.width // 3  # put this in center top
        score_rect.top = 10

        round_text = self.font.render("ROUND: " + str(self.round_number), True, white)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20, 10)  # put this in top left

        # lives_text = self.font.render("LIVES: " + str(self.player.lives), True, white)
        # lives_rect = lives_text.get_rect()
        # lives_rect.topright = (width - 20, 10)

        accuracy_text = self.font.render("ACCURACY: " + str(self.player.accuracy) + "%", True, white)
        accuracy_rect = accuracy_text.get_rect()
        accuracy_rect.topright = (self.width * 0.7, 10)

        lives = pygame.image.load("images/Love_Heart.png")
        lives = pygame.transform.scale(lives, (53, 53))

        for j in range(self.player.lives):
            lives_rect = lives.get_rect()
            lives_rect.topright = (self.width - 40 * j, 2)
            self.display_surface.blit(lives, lives_rect)

        # Blitting the text to the display
        self.display_surface.blit(score_text, score_rect)
        self.display_surface.blit(round_text, round_rect)
        # display_surface.blit(lives_text, lives_rect)
        self.display_surface.blit(accuracy_text, accuracy_rect)

        pygame.draw.line(self.display_surface, white, (0, 50), (self.width, 50), 4)
        pygame.draw.line(self.display_surface, white, (0, self.height - 120), (self.width, self.height - 120), 4)

    def shift_aliens(self):
        # shift aliens
        # Determine if alien group has hit an edge
        shift = False
        for alien in (self.alien_group.sprites()):
            if alien.rect.left <= 0 or alien.rect.right >= self.width:
                shift = True
        for chest in (self.chest_group.sprites()):
            if chest.rect.left <= 0 or chest.rect.right >= self.width:
                shift = True

        # Shift every alien down, change direction and check if they cross the bottom line
        if shift:
            breach = False
            for alien in (self.alien_group.sprites()):
                # Shift down
                alien.rect.y += 10 * self.round_number
                # Reverse the direction and move the alien off the edge
                alien.direction = -1 * alien.direction  # reverse
                alien.rect.x += alien.direction * alien.velocity

                # Check if an alien reached the ship
                if alien.rect.bottom >= self.height - 50:
                    breach = True

            # Aliens breached the line
            if breach:
                self.breach_sound.play()  # play sound
                self.player.lives -= 1  # remove a life
                self.check_game_status("Oh dear! Aliens have reached the International Space Station!",
                                       "Please press 'Enter' to defend again!")

            self.shift_chest()

    def shift_chest(self):
        # Shift every chest down, change direction and check if they cross the bottom line
        for chest in (self.chest_group.sprites()):
            # Shift down
            chest.rect.y += 10 * self.round_number
            # Reverse the direction and move the chest off the edge
            chest.direction = -1 * chest.direction  # reverse
            chest.rect.x += chest.direction * chest.velocity

            # Check if a chest reached the ship
            if chest.rect.bottom >= self.height - 50:
                chest.kill()

    def check_collisions(self):
        # check for collisions
        # See if any bullet in the player bullet group hits an alien in the alien group
        if pygame.sprite.groupcollide(self.player_bullet_group, self.alien_group, True,
                                      True):  # ie kill bullet and kill alien
            self.alien_hit_sound.play()
            self.score += 100
            self.player.hits += 1
            self.player.update_accuracy()
        elif pygame.sprite.groupcollide(self.player_bullet_group, self.chest_group, True,
                                        True):  # ie kill bullet and kill chest
            self.chest_hit_sound.play()
            self.score += 500
            self.player.boost = True
            self.player.hits += 1
            self.player.update_accuracy()

        elif pygame.sprite.groupcollide(self.player_bullet_group, self.heart_group, True,
                                        True):  # ie kill bullet and kill heart
            self.heart_hit_sound.play()
            self.player.hits += 1
            self.player.update_accuracy()
            # Capping lives at 5
            if self.player.lives < 5:
                self.player.lives += 1
            else:
                self.player.lives = 5

        # See if player has collided with any bullet in the alien bullet group
        if pygame.sprite.spritecollide(self.player, self.alien_bullet_group, True):
            self.player_hit_sound.play()
            self.player.lives -= 1  # remove a life
            self.check_game_status("Oh no! You've been hit!",
                                   "Press 'Enter' to continue to defend the ISS from Aliens!")

    def check_round_completion(self):
        # check to see if a player has completed a single round
        if not self.alien_group:  # If there is not a single sprite.
            for bullet in self.player_bullet_group:
                bullet.kill()
            for chest in self.chest_group:
                chest.kill()
            self.player.reset()
            self.score += 1000 * self.round_number  # score bonus
            self.round_number += 1
            self.start_new_round()

    def start_new_round(self):
        # start a new round
        # Create a grid of aliens, 11 columns and 5 rows
        random_column = randint(1, 10)
        heart = Heart(self.width + 10, 10, self.round_number, self.heart_group, self.heart_bullet_group, self.width,
                      self.height)
        self.heart_group.add(heart)
        for i in range(10):
            for j in range(5):
                if j == 0 and i == random_column - 1:
                    chest = Chest(64 + i * 64, 64 + 64 * j, self.round_number, self.chest_group,
                                  self.chest_bullet_group, self.width,
                                  self.height)  # make the velocity speed up as the rounds go by
                    self.chest_group.add(chest)

                else:
                    alien = Alien(64 + i * 64, 64 + 64 * j, self.round_number, self.alien_group,
                                  self.alien_bullet_group, self.width,
                                  self.height)  # make the velocity speed up as the rounds go by
                    self.alien_group.add(alien)

        # Pause the game and prompt the user to start
        self.new_round_sound.play()
        self.pause_game("Space Invaders Round " + str(self.round_number),
                        "Press 'Enter' to defend the International Space Station from Aliens!")

    def check_game_status(self, main_text, sub_text):
        # check to see the status of a game and how the player died
        # Empty the bullet groups and reset the player and remaining aliens
        for bullet in self.player_bullet_group:
            bullet.kill()
        self.player_bullet_group.empty()
        self.alien_bullet_group.empty()
        self.chest_bullet_group.empty()
        self.player.reset()  # we made this function earlier
        for alien in self.alien_group:
            alien.reset()
        for chest in self.chest_group:
            chest.kill()

        # Check if player has enough lives
        if self.player.lives == 0:
            self.reset_game()
        else:
            self.pause_game(main_text, sub_text)

    def pause_game(self, main_text, sub_text):
        # Set colors
        white = (255, 255, 255)

        # Create main pause text
        main_text = self.font.render(main_text, True, white)
        main_rect = main_text.get_rect()
        main_rect.center = (self.width // 2, self.height // 2)

        # Create sub text
        sub_text = self.font.render(sub_text, True, white)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (self.width // 2, self.height // 2 + 53)

        # Blit the pause text
        self.display_surface.fill((236, 198, 230))
        self.display_surface.blit(main_text, main_rect)
        self.display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        # Pause the game until the user hits enter
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # The user wants to play again
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                # If the user sadly wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    self.running = False

    def reset_game(self):
        # reset the game
        self.pause_game("Final Score: " + str(self.score) + "     Accuracy of " + str(self.player.accuracy) + "%",
                        "Press 'Enter' to defend the International Space Station again!")

        # Reset game values
        self.score = 0
        self.round_number = 1
        self.player.lives = 5
        self.player.boost = False
        self.player.boost_timer = self.fps * 3
        self.player.hits = 0
        self.player.accuracy = 0.0
        self.player.attempts = 0

        # Empty groups
        self.alien_group.empty()
        self.chest_group.empty()
        self.heart_group.empty()
        self.player_bullet_group.empty()
        self.alien_bullet_group.empty()
        self.chest_bullet_group.empty()
        self.heart_bullet_group.empty()

        # Start a new game
        self.start_new_round()
