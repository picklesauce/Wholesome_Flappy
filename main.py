import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BIRD_WIDTH, BIRD_HEIGHT = 50, 35
PIPE_WIDTH, PIPE_HEIGHT = 50, 300
PIPE_GAP = 200
FPS = 60

# Colors
SKY_BLUE = (135, 206, 250)  # Sky blue color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load bird image
bird_image = pygame.image.load("images/bird1.png")  # Replace "bird.png" with your actual bird image file

pipe_image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT), pygame.SRCALPHA)
pygame.draw.rect(pipe_image, (0, 255, 0), (0, 0, PIPE_WIDTH, PIPE_HEIGHT // 2))
pygame.draw.rect(pipe_image, (0, 255, 0), (0, PIPE_HEIGHT // 2 + PIPE_GAP, PIPE_WIDTH, HEIGHT - (PIPE_HEIGHT // 2 + PIPE_GAP)))

# Clock to control the frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Function to draw text on the screen
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to draw the bird
def draw_bird(x, y):
    screen.blit(bird_image, (x, y))

# Function to draw pipes
def draw_pipe(x, height):
    screen.blit(pipe_image, (x, 0), (0, 0, PIPE_WIDTH, height))
    screen.blit(pipe_image, (x, height + PIPE_GAP), (0, 0, PIPE_WIDTH, HEIGHT - (height + PIPE_GAP)))

# Function to draw clouds
def draw_cloud(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), 20)
    pygame.draw.circle(screen, WHITE, (x + 30, y), 25)
    pygame.draw.circle(screen, WHITE, (x + 60, y), 20)

# Function to draw the sun
def draw_sun(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), 50)

# Game loop
def game_loop():
    bird_x = 50
    bird_y = HEIGHT // 2 - BIRD_HEIGHT // 2
    bird_velocity = 0

    pipe_x = WIDTH
    pipe_height = random.randint(50, HEIGHT - 200)

    cloud_x = random.randint(0, WIDTH)
    cloud_y = random.randint(20, 150)

    sun_x = 500
    sun_y = 50

    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = -8

        # Bird physics
        bird_y += bird_velocity
        bird_velocity += 0.5

        # Pipe movement
        pipe_x -= 5

        # Cloud movement
        cloud_x -= 1
        if cloud_x < -100:
            cloud_x = WIDTH + random.randint(100, 300)
            cloud_y = random.randint(20, 150)

        # Check for collision
        if (
            bird_x + BIRD_WIDTH > pipe_x
            and bird_x < pipe_x + PIPE_WIDTH
            and (bird_y < pipe_height or bird_y + BIRD_HEIGHT > pipe_height + PIPE_GAP)
        ):
            game_over()

        # Check if the pipe has passed the bird
        if pipe_x < bird_x - BIRD_WIDTH - PIPE_WIDTH:
            pipe_x = WIDTH
            pipe_height = random.randint(50, HEIGHT - 200)
            score += 1

        # Check if the bird is out of the screen
        if bird_y > HEIGHT or bird_y < 0:
            game_over()

        # Draw everything
        screen.fill(SKY_BLUE)  # Set the background color to sky blue
        draw_sun(sun_x, sun_y)
        draw_cloud(cloud_x, cloud_y)
        draw_cloud(cloud_x + 200, cloud_y + 50)
        draw_cloud(cloud_x + 400, cloud_y - 20)
        draw_bird(bird_x, bird_y)
        draw_pipe(pipe_x, pipe_height)
        draw_text(f"Score: {score}", 10, 10, BLACK)

        # Update the display
        pygame.display.update()

        # Set the frame rate
        clock.tick(FPS)

# Function to display game over screen
def game_over():
    screen.fill(WHITE)
    draw_text("Game Over", WIDTH // 2 - 100, HEIGHT // 2 - 50, BLACK)
    pygame.display.update()
    pygame.time.wait(2000)  # Wait for 2 seconds
    game_loop()

# Run the game
game_loop()