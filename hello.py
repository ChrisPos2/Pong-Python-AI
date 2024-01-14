import pygame
pygame.init()

# Constants
width, height = 800, 600
paddle_width, paddle_height = 10, 100
paddle_speed = 5
background_color = (0, 0, 0)
paddle_color = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")

# Initialize the left paddle
paddle_x = 10  # X-coordinate of the left paddle
paddle_y = (height - paddle_height) // 2  # Centered vertically

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  # Move the paddle up with the 'W' key
        paddle_y -= paddle_speed
    if keys[pygame.K_s]:  # Move the paddle down with the 'S' key
        paddle_y += paddle_speed

    # Ensure the paddle doesn't go out of the screen bounds
    paddle_y = max(0, min(paddle_y, height - paddle_height))

    # Clear the screen
    screen.fill(background_color)
    
    # Draw game objects
    pygame.draw.rect(screen, paddle_color, (paddle_x, paddle_y, paddle_width, paddle_height))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)

pygame.quit()
