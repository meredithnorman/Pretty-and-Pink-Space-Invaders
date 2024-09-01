import pygame, random, math

# Initialise pygame
pygame.init()

# Set display surface
width =1200
height = 900
display_surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

# Setting the working directory
import os

os.chdir('Your working directory')

# Set Frames per second and clock
FPS = 60
clock = pygame.time.Clock()
BOOST_TIME_IN_SECS = 4


# Define classes

class Game():
    # A class to help control and update gameplay

    def __init__(self, player, alien_group, chest_group, love_heart_group, player_bullet_group, alien_bullet_group, chest_bullet_group, love_heart_bullet_group):
        # initialise the game
        # Set game values
        self.round_number = 1
        self.score = 0
        self.player = player
        self.alien_group = alien_group
        self.chest_group = chest_group
        self.love_heart_group=love_heart_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group
        self.chest_bullet_group = chest_bullet_group
        self.love_heart_bullet_group=love_heart_bullet_group


        # Set sounds and music
        self.new_round_sound = pygame.mixer.Sound("new_round.wav")
        self.breach_sound = pygame.mixer.Sound("breach.wav")  # i.e the aliens 'breach' the bounds of the screen
        self.alien_hit_sound = pygame.mixer.Sound("alien_hit.wav")
        self.player_hit_sound = pygame.mixer.Sound("player_hit.wav")
        self.chest_hit_sound = pygame.mixer.Sound("bonus_acquired.wav")
        self.heart_hit_sound=pygame.mixer.Sound("heart_wav.wav")

        # Set font
        self.font = pygame.font.SysFont('candara', 32, bold=10)

    def update(self):
        # update the game
        self.shift_aliens()
        self.check_collisions()
        self.check_round_completition()

    def draw(self):
        # Draw information to the display
        white = (255, 255, 255)

        # Set text
        score_text = self.font.render("SCORE: " + str(self.score), True, white)
        score_rect = score_text.get_rect()
        score_rect.centerx = width // 3  # put this in center top
        score_rect.top = 10

        round_text = self.font.render("ROUND: " + str(self.round_number), True, white)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20, 10)  # put this in top left

        lives_text = self.font.render("LIVES: " + str(self.player.lives), True, white)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (width - 20, 10)

        accuracy_text = self.font.render("ACCURACY: " + str(self.player.accuracy)+ "%", True, white)
        accuracy_rect = accuracy_text.get_rect()
        accuracy_rect.topright = (width*0.7, 10)

        # Blitting the text to the display
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(accuracy_text, accuracy_rect)

        pygame.draw.line(display_surface, white, (0, 50), (width, 50), 4)
        pygame.draw.line(display_surface, white, (0, height - 120), (width, height - 120), 4)

    def shift_aliens(self):
        # shift aliens
        # Determine if alien group has hit an edge
        shift = False
        for alien in (self.alien_group.sprites()):
            if alien.rect.left <= 0 or alien.rect.right >= width:
                shift = True
        for chest in (self.chest_group.sprites()):
            if chest.rect.left <= 0 or chest.rect.right >= width:
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
                if alien.rect.bottom >= height - 50:
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
            if chest.rect.bottom >= height - 50:
                chest.kill()

    
    
    

    def check_collisions(self):
        # check for collisions
        # See if any bullet in the player bullet group hits an alien in the alien group
        if pygame.sprite.groupcollide(self.player_bullet_group, self.alien_group, True,
                                      True):  # ie kill bullet and kill alien
            self.alien_hit_sound.play()
            self.score += 100
            self.player.hits+=1
            self.player.update_accuracy()
        elif pygame.sprite.groupcollide(self.player_bullet_group, self.chest_group, True,
                                        True):  # ie kill bullet and kill chest
            self.chest_hit_sound.play()
            self.score += 500
            self.player.boost = True
            self.player.hits+=1
            self.player.update_accuracy()
        
        elif pygame.sprite.groupcollide(self.player_bullet_group, self.love_heart_group, True,
                                        True):  # ie kill bullet and kill heart
            self.heart_hit_sound.play()
            self.player.lives += 1
            self.player.hits+=1
            self.player.update_accuracy()

        

        # See if player has collided with any bullet in the alien bullet group
        if pygame.sprite.spritecollide(self.player, self.alien_bullet_group, True):
            self.player_hit_sound.play()
            self.player.lives -= 1  # remove a life
            self.check_game_status("Oh no! You've been hit!",
                                   "Press 'Enter' to continue to defend the ISS from Aliens!")

    def check_round_completition(self):
        # check to see if a player has completed a single round
        if not (self.alien_group):  # If there is not a single sprite.
            for bullet in my_player_bullet_group:
                bullet.kill()
            for chest in my_chest_group:
                chest.kill()
            self.player.reset()
            self.score += 1000 * self.round_number  # score bonus
            self.round_number += 1
            self.start_new_round()

    def start_new_round(self):
        # start a new round
        # Create a grid of alliens, 11 columns and 5 rows
        random_column = random.randint(1, 10)
        love_heart=Love_Heart(width+10, 10, self.round_number, self.love_heart_bullet_group)
        self.love_heart_group.add(love_heart)
        for i in range(10):
            for j in range(5):
                if j == 0 and i == random_column - 1:
                    chest = Chest(64 + i * 64, 64 + 64 * j, self.round_number,
                                  self.chest_bullet_group)  # make the velocity speed up as the rounds go by
                    self.chest_group.add(chest)

                else:
                    alien = Alien(64 + i * 64, 64 + 64 * j, self.round_number,
                                  self.alien_bullet_group)  # make the velocity speed up as the rounds go by
                    self.alien_group.add(alien)

        

        # Pause the game and prompt the user to start
        self.new_round_sound.play()
        self.pause_game("Space Invaders Round " + str(self.round_number),
                        "Press 'Enter' to defend the International Space Station from Aliens!")

    def check_game_status(self, main_text, sub_text):
        # check to see the status of a game and how the player died
        # Empty the bullet groups and reset the player and remaining aliens
        for bullet in my_player_bullet_group:
            bullet.kill()
        self.alien_bullet_group.empty()
        self.chest_bullet_group.empty()
        self.player_bullet_group.empty()
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
        global running  # making running a global variable so you can access it outside the function.
        # pause the game
        # Set colors
        white = (255, 255, 255)

        # Create main pause text
        main_text = self.font.render(main_text, True, white)
        main_rect = main_text.get_rect()
        main_rect.center = (width // 2, height // 2)

        # Create sub text
        sub_text = self.font.render(sub_text, True, white)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (width // 2, height // 2 + 53)

        # Blit the pause text
        display_surface.fill((236, 198, 230))
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
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
                    running = False

    def reset_game(self):
        # reset the game
        self.pause_game("Final Score: " + str(self.score) + "     Accuracy of " + str(self.player.accuracy) + "%",
                        "Press 'Enter' to defend the International Space Station again!")

        # Reset game values
        self.score = 0
        self.round_number = 1
        self.player.lives = 5
        self.player.boost = False
        self.player.boost_timer = FPS * 3
        self.player.hits=0
        self.player.accuracy=0.0
        self.player.attempts=0

        # Empty groups
        self.alien_group.empty()
        self.chest_group.empty()
        self.love_heart_group.empty()
        self.alien_bullet_group.empty()
        self.chest_bullet_group.empty()
        self.player_bullet_group.empty()
        self.love_heart_bullet_group.empty()

        # Start a new game
        self.start_new_round()


class Player(pygame.sprite.Sprite):  # use the sprite.Sprite as you have to inherit from the game class
    # A class to model a spaceship the user can control

    def __init__(self, bullet_group):
        # Initialise the player
        super().__init__()
        self.image = pygame.image.load("Ship.png")
        ship_size = (100, 100)  # resizing the ship
        self.image = pygame.transform.scale(self.image, ship_size)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height  # so positioning the ship in the center at the bottom of the screen.

        self.lives = 5
        self.velocity = 8

        self.bullet_group = bullet_group

        self.boost = False
        self.boost_timer = FPS * BOOST_TIME_IN_SECS
        self.shoot_sound_boost = pygame.mixer.Sound("laser_fire.mp3")
        self.shoot_sound_normal = pygame.mixer.Sound("player_fire.wav")

        self.accuracy=0.0
        self.hits=0
        self.attempts=0


    def update(self):
        # update the player
        keys = pygame.key.get_pressed()

        # move the player within the bounds of the screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.velocity

        if self.boost:
            self.boost_timer -= 1
        if self.boost_timer == 0:
            self.boost = False
            self.boost_timer = FPS * BOOST_TIME_IN_SECS

    def fire(self):
        self.attempts+=1
        self.update_accuracy()
        # Fire a bullet
        if self.boost:
            self.shoot_sound_boost.play()
        else:
            self.shoot_sound_normal.play()
        PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group,
                     self.boost)  # fire from the top of the ship. We are using the Player Bullet class and have to put in all the neccessary inputs.
        
    def update_accuracy(self):    #Making a function seemed like the easiest way to calculate and update accuracy
        if self.attempts > 0:
            self.accuracy = round((self.hits / self.attempts) * 100,1) 
        else:
            self.accuracy = 0   #make sure that you don't just get//0 

    def reset(self):
        # Reset the players position
        self.rect.centerx = width // 2
        self.boost = False
        self.boost_timer = FPS * BOOST_TIME_IN_SECS


class Alien(pygame.sprite.Sprite):  # use the sprite.Sprite as you have to inherit from the game class
    # A class to model an enemy alien

    def __init__(self, x, y, velocity, bullet_group):
        # Initialise the alien
        super().__init__()
        self.image = pygame.image.load("purple_invader.svg")
        alien_size = (87, 87)  # resizing the ship
        self.image = pygame.transform.scale(self.image, alien_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.starting_x = x  # This aims to make resetting the aliens alot easier.
        self.starting_y = y

        self.direction = 1  # Positive 1 is moving to the right, -1 is moving to the left.
        self.velocity = velocity
        self.bullet_group = bullet_group

        self.shoot_sound = pygame.mixer.Sound("alien_fire.wav")

        
    def update(self):
        # update the alien
        self.rect.x += self.direction * self.velocity  # ie left or right and then velocity

        # Randomly fire a bullet
        if random.randint(0, 3000) > (2995)+0.06*len(my_alien_group) and len(my_alien_bullet_group) < 3:  
            # When there are less aliens, the probability of shooting increases slightly. This probably isn't the most optimal way of doing it. I also make sure there are max 3 bullets at once fron the aliens. 
            self.fire()

    def fire(self):
        # Fire a bullet
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

    def reset(self):
        # Reset the aliens position
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.direction = 1


class Chest(Alien):
    # A class to model a treasure chest

    def __init__(self, x, y, velocity, bullet_group):
        super().__init__(x, y, velocity, bullet_group)
        self.image = pygame.image.load("treasure_chest.png")
        chest_size = (50, 50)  # resizing the ship
        self.image = pygame.transform.scale(self.image, chest_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.starting_x = x  # This aims to make resetting the aliens alot easier.
        self.starting_y = y

        self.direction = 1  # Positive 1 is moving to the right, -1 is moving to the left.
        self.velocity = velocity
        self.bullet_group = bullet_group

        self.shoot_sound = pygame.mixer.Sound("alien_fire.wav")

    def fire(self):
        pass

class Love_Heart(Alien, pygame.sprite.Sprite):
    # A class to model a love heart which will give the player an extra life 

    def __init__(self, x, y, velocity, bullet_group):
        super().__init__(x, y, velocity, bullet_group)
        self.image = pygame.image.load("Love_Heart.png")
        heart_size = (100, 100)  # resizing the heart
        self.image = pygame.transform.scale(self.image, heart_size)
        self.rect = self.image.get_rect()
        self.rect.x = width-100  # Initial x position
        self.rect.y = 75  # Initial y position
        self.time = 0  # Initialize time to control oscillation
        self.amplitude = 75  # Oscillation amplitude (height of the sine wave)
        self.frequency = 0.05  # Oscillation frequency (controls speed of the sine wave)

        self.starting_x = x  # This aims to make resetting the aliens alot easier.
        self.starting_y = y

       
        self.velocity = 1      # choosing to be very kind and making the heart speed consistent even when the rounds progress.
        self.bullet_group = bullet_group  

    def update(self):
        self.oscillate()

    def oscillate(self):
        # Update the x position using a sine wave for oscillation
        self.rect.x -= self.velocity #move at a different rate compared to the aliens
        self.rect.y = 200 + self.amplitude * math.sin(self.time)
        self.time += self.frequency  # Increment time to create oscillation


class PlayerBullet(pygame.sprite.Sprite):
    # A class to model a bullet fired by the player

    def __init__(self, x, y, bullet_group,
                 boost):  # The bullet group aims to minimise the number of bullets on the screen at any given time.
        # Initialise the bullet
        super().__init__()
        self.boost = boost
        if self.boost:
            self.image = pygame.image.load("boost_laser.png")
        else:
            self.image = pygame.image.load("green_laser.png")
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

    # Note we are checking for collisions inside of our game object so we don't need to here.


class AlienBullet(pygame.sprite.Sprite):
    # A class to model a bullet fired by the alien

    def __init__(self, x, y, bullet_group):
        # Initialise the bullet
        super().__init__()
        self.image = pygame.image.load("red_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        # update the bullet
        self.rect.y += self.velocity

        # If the bullet is off the screen, remove it.
        if self.rect.top > height:
            self.kill()  # kill is dramatic
    # Note we are checking for collisions inside of our game object so we don't need to here.


# Create bullet groups
my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group()
my_chest_bullet_group = pygame.sprite.Group()
my_love_heart_bullet_group=pygame.sprite.Group()

# Create a player group and player object
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)  # so that the player class has access to the bullet class.
my_player_group.add(my_player)

# Create an alien group. Will add Alien objects via the game's start new round method.
my_alien_group = pygame.sprite.Group()

# Create a chest group. Will add Chest objects via the game's start new round method.
my_chest_group = pygame.sprite.Group()

#Create a love heart group
my_love_heart_group=pygame.sprite.Group()

# Create a game object
my_game = Game(my_player, my_alien_group, my_chest_group,my_love_heart_group, my_player_bullet_group, my_alien_bullet_group,
               my_chest_bullet_group, my_love_heart_bullet_group)
my_game.start_new_round()

# The main game loop
running = True
while running:
    # Check to see if the user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    my_love_heart_group.update()
    my_love_heart_group.draw(display_surface)

    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(display_surface)

    my_chest_bullet_group.update()
    my_chest_bullet_group.draw(display_surface)

    my_love_heart_bullet_group.update()
    my_love_heart_bullet_group.draw(display_surface)



    # Update and draw object
    my_game.update()
    my_game.draw()

    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()

