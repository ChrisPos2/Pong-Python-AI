import pygame
pygame.init()

# Constants
width, height = 800, 600
paddle_width, paddle_height = 10, 100
paddle_speed = 5
background_color = (0, 0, 0)
paddle_color = (255, 255, 255)

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = paddle_width
        self.height = paddle_height

    def move_up(self):
        self.y -= paddle_speed

    def move_down(self):
        self.y += paddle_speed

    def limit_y(self):
        self.y = max(0, min(self.y, height - self.height))

    def draw(self, screen):
        pygame.draw.rect(screen, paddle_color, (self.x, self.y, self.width, self.height))

# Initialize the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")

# Initialize the left paddle
left_paddle = Paddle(10, (height - paddle_height) // 2)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_paddle.move_up()
    if keys[pygame.K_s]:
        left_paddle.move_down()

    left_paddle.limit_y()

    # Clear the screen
    screen.fill(background_color)
    
    # Draw game objects
    left_paddle.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)

pygame.quit()
