import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-Ball Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle properties
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
PADDLE_SPEED = 5

# Ball properties
BALL_SIZE = 15
BALL_SPEED = 5
NUM_BALLS = 3  # Number of balls in the game

# Create paddles
player = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create multiple balls
balls = []
for _ in range(NUM_BALLS):
    ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
    ball_speed_x = BALL_SPEED * random.choice((1, -1))
    ball_speed_y = BALL_SPEED * random.choice((1, -1))
    balls.append({'rect': ball, 'speed_x': ball_speed_x, 'speed_y': ball_speed_y})

# Score
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.top > 0:
        player.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player.bottom < HEIGHT:
        player.y += PADDLE_SPEED

    # Opponent AI
    # Simple AI tracks the first ball (could be modified to track closest ball)
    if opponent.centery < balls[0]['rect'].centery and opponent.bottom < HEIGHT:
        opponent.y += PADDLE_SPEED
    if opponent.centery > balls[0]['rect'].centery and opponent.top > 0:
        opponent.y -= PADDLE_SPEED

    # Ball movement and collisions
    for ball in balls:
        ball['rect'].x += ball['speed_x']
        ball['rect'].y += ball['speed_y']

        # Ball collision with top and bottom
        if ball['rect'].top <= 0 or ball['rect'].bottom >= HEIGHT:
            ball['speed_y'] = -ball['speed_y']

        # Ball collision with paddles
        if ball['rect'].colliderect(player) or ball['rect'].colliderect(opponent):
            ball['speed_x'] = -ball['speed_x']

        # Scoring
        if ball['rect'].left <= 0:
            opponent_score += 1
            ball['rect'].center = (WIDTH//2, HEIGHT//2)
            ball['speed_x'] = BALL_SPEED * random.choice((1, -1))
            ball['speed_y'] = BALL_SPEED * random.choice((1, -1))
        
        if ball['rect'].right >= WIDTH:
            player_score += 1
            ball['rect'].center = (WIDTH//2, HEIGHT//2)
            ball['speed_x'] = BALL_SPEED * random.choice((1, -1))
            ball['speed_y'] = BALL_SPEED * random.choice((1, -1))

    # Drawing
    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, player)
    pygame.draw.rect(window, WHITE, opponent)
    for ball in balls:
        pygame.draw.ellipse(window, WHITE, ball['rect'])
    pygame.draw.aaline(window, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Draw score
    player_text = font.render(str(player_score), False, WHITE)
    opponent_text = font.render(str(opponent_score), False, WHITE)
    window.blit(player_text, (WIDTH//4, 20))
    window.blit(opponent_text, (3*WIDTH//4, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
