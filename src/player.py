import pygame
import sys

# Initialize Pygame
pygame.init()     

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Player Class in Pygame")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, name, health=100, strength=10, defense=5):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.name = name
        self.health = health
        self.strength = strength
        self.defense = defense

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

# Create two players
player1 = Player(200, 300, "Player 1")
player2 = Player(600, 300, "Player 2")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keyboard buttons
    keys = pygame.key.get_pressed()

    # Player 1 movement (WASD)
    if keys[pygame.K_w]:
        player1.move(0, -5)
    if keys[pygame.K_s]:
        player1.move(0, 5)
    if keys[pygame.K_a]:
        player1.move(-5, 0)
    if keys[pygame.K_d]:
        player1.move(5, 0)

    # Player 2 movement (Arrow keys)
    if keys[pygame.K_UP]:
        player2.move(0, -5)
    if keys[pygame.K_DOWN]:
        player2.move(0, 5)
    if keys[pygame.K_LEFT]:
        player2.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        player2.move(5, 0)

    # Display players
    screen.fill(WHITE)
    screen.blit(player1.image, player1.rect)
    screen.blit(player2.image, player2.rect)

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
