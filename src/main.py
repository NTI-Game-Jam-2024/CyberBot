import random
import sys

import pygame

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Sprite Example')

# Load the images
start_background = pygame.image.load("start_background.png").convert()
game_background = pygame.image.load("game_background.png").convert()

player_image = pygame.image.load('player.png')
enemy_image = pygame.image.load('enemy_melee.png')

RED = (255, 0, 0)
WHITE = (255, 255, 255)


# Define player
class Player():
    def __init__(self, x, y):
        image = pygame.image.load('player.png')
        self.x = x
        self.y = y
        self.soldier = image.convert_alpha()
        self.rect = self.soldier.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.is_jumping = False
        self.jump_count = 10  # initial jump velocity
        self.max_health = 2000  # Set maximum health
        self.health = self.max_health

    def update(self):
        # Get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= 5
        if key[pygame.K_d]:
            self.rect.x += 5
        if key[pygame.K_w] and not self.is_jumping:
            self.is_jumping = True

        pygame.display.update()
      
        # Jump logic
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.3 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10

        # Check if health is below 0
        if self.health <= 0:
            print("Game Over!")
            pygame.quit()
            sys.exit()

    def draw_health_bar(self, surface):
        # Calculate health bar width based on current health
        health_bar_width = (self.health / self.max_health) * 100
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, health_bar_width, 10))
        pygame.draw.rect(surface, WHITE, (self.rect.x, self.rect.y - 10, 100, 10), 2)



pygame.display.flip()

# Define enemy
class Enemy():
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.enemy = enemy_image.convert_alpha()
        self.rect = self.enemy.get_rect()
        self.rect.bottomleft = (self.x, self.y)  # Set enemy at the player's feet level
        self.player = player
        self.speed = 1  # Adjust enemy speed
    
    pygame.display.flip()
  
    def update(self):
        # Movement logic
        if self.rect.x < self.player.rect.x:
            self.rect.x += self.speed  # Move right towards the player
        elif self.rect.x > self.player.rect.x:
            self.rect.x -= self.speed  # Move left towards the player

        # Collision detection
        if self.rect.colliderect(self.player.rect):
            self.player.health -= 1  # Deal 2 damage to the player
            print("Collision detected! Player Health:", self.player.health)


player = Player(50, 175)
enemies = [Enemy(random.randint(50, 350), player.rect.bottom, player) for _ in range(3)]  # Create 3 enemies
clock = pygame.time.Clock()

# Define game states
START_SCREEN = 0
GAME_SCREEN = 1
current_screen = START_SCREEN

# Main game loop
run = True
while run:
    clock.tick(60)

    # Update and draw enemies
    for enemy in enemies:
        enemy.update()
        screen.blit(enemy.enemy, enemy.rect)

    player.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif current_screen == START_SCREEN and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Check for spacebar key press
            current_screen = GAME_SCREEN

    # Render current screen
    if current_screen == START_SCREEN:
        screen.blit(start_background, (0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
    elif current_screen == GAME_SCREEN:
        screen.blit(game_background, (0, 0))
        screen.blit(player.soldier, player.rect)
        player.draw_health_bar(screen)  # Draw player's health bar

    pygame.display.flip()

pygame.quit()
