import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(GREEN)
        pygame.draw.polygon(self.image, WHITE, [(25, 0), (0, 30), (50, 30)])  # Triangle ship
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 5
        self.shoot_cooldown = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        self.shoot_cooldown = max(0, self.shoot_cooldown - 1)

    def shoot(self):
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            player_bullets.add(bullet)
            self.shoot_cooldown = 20  # Frames between shots

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10  # Negative to move up

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        pygame.draw.rect(self.image, BLACK, (10, 5, 20, 20))  # Simple alien design
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 2
        self.move_counter = 0
        self.move_down = False

    def update(self):
        self.move_counter += 1
        self.rect.x += self.speed_x
        
        # Move down and reverse direction every 50 frames
        if self.move_counter >= 50:
            self.move_down = True
            self.speed_x = -self.speed_x
            self.move_counter = 0
        
        if self.move_down:
            self.rect.y += 20
            self.move_down = False
        
        # Respawn at top if off bottom
        if self.rect.top > HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, WIDTH - self.rect.width)

# Sprite groups
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Initialize player
player = Player()
all_sprites.add(player)

# Spawn initial enemies (3 rows of 8)
for row in range(3):
    for col in range(8):
        enemy = Enemy(col * 60 + 50, row * 50 + 50)
        all_sprites.add(enemy)
        enemies.add(enemy)

# Game variables
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Check collisions (bullets and enemies)
    hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
    for hit in hits:
        score += 10
        # Respawn enemy at top
        new_enemy = Enemy(random.randint(0, WIDTH - 40), -40)
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)

    # Check player-enemy collision
    if pygame.sprite.spritecollide(player, enemies, False):
        running = False  # Game over on collision

    # Draw
    window.fill(BLACK)
    all_sprites.draw(window)

    # Draw score
    score_text = font.render(f"Score: {score}", False, WHITE)
    window.blit(score_text, (10, 10))

    pygame.display.flip()

# Game over
game_over_text = font.render(f"Game Over! Final Score: {score}", False, WHITE)
window.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
sys.exit()
