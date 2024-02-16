import random
import sys

import pygame

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Sprite Example')
game_font = pygame.font.SysFont("Arial", 30)

# Load the images
start_background = pygame.image.load("assets/start_background.png").convert()
game_background = pygame.image.load("assets/game_background.png").convert()

RED = (255, 0, 0)
WHITE = (255, 255, 255)


def game_over_screen():
  waiting_for_input = True
  while waiting_for_input:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          return True

    screen.fill(pygame.Color("black"))
    game_over_text = game_font.render("Game Over! Press Enter to Restart",
                                      True, (255, 255, 255))
    screen.blit(
        game_over_text,
        (width // 2 - game_over_text.get_width() // 2, height // 2),
    )
    pygame.display.flip()
    clock.tick(15)

  return False


# Define player
class Player():

  def __init__(self, x, y):
    image = pygame.image.load('assets/player.png')
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

    # Jump logic
    if self.is_jumping:
      if self.jump_count >= -10:
        neg = 1
        if self.jump_count < 0:
          neg = -1
        self.rect.y -= (self.jump_count**2) * 0.3 * neg
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
    pygame.draw.rect(surface, RED,
                     (self.rect.x, self.rect.y - 10, health_bar_width, 10))
    pygame.draw.rect(surface, WHITE, (self.rect.x, self.rect.y - 10, 100, 10),
                     2)


pygame.display.flip()


class Enemy:

  def __init__(self, x, y, player):
    self.enemy = pygame.image.load('assets/enemy_melee.png')
    self.rect = self.enemy.get_rect(bottomleft=(x, y))
    self.player = player
    self.speed = 1  # Adjust enemy speed

  def update(self):
    # Movement logic
    if self.rect.x < self.player.rect.x:
      self.rect.x += self.speed
    elif self.rect.x > self.player.rect.x:
      self.rect.x -= self.speed

    # Collision detection
    if self.rect.colliderect(self.player.rect):
      self.player.health -= 1  # Deal 1 damage to the player
      print("Collision detected! Player Health:", self.player.health)


player = Player(50, 175)
enemies = [
    Enemy(random.randint(50, 350), player.rect.bottom, player)
    for _ in range(3)
]  # Create 3 enemies
clock = pygame.time.Clock()

# Define game states
START_SCREEN = 0
GAME_SCREEN = 1
current_screen = START_SCREEN

# Main game loop
run = False
while not run:
  screen.fill(WHITE)
  start_background = pygame.image.load("assets/start_background.png").convert()
  screen.blit(start_background, (0, 0))

  pygame.display.flip()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      run = True
      start_time = pygame.time.get_ticks()
while run is True:
  clock.tick(60)

  screen.fill(WHITE)

  # Update and draw enemies
  for enemy in enemies:
    enemy.update()
    screen.blit(enemy.enemy, enemy.rect)

  player.update()
  screen.blit(player.soldier,
              player.rect)  # Blit player image directly onto the screen
  player.draw_health_bar(screen)  # Draw player's health bar

  # Event handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.flip()

  if player.health == 0:
    game_over_screen()

pygame.quit()
