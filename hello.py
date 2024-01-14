import pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 5
BACKGROUND_COLOR = (0, 0, 0)
PADDLE_COLOR = (255, 255, 255)

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT

    def move_up(self):
        self.y -= PADDLE_SPEED

    def move_down(self):
        self.y += PADDLE_SPEED

    def limit_y(self):
        self.y = max(0, min(self.y, HEIGHT - self.height))

    def draw(self, screen):
        pygame.draw.rect(screen, PADDLE_COLOR, (self.x, self.y, self.width, self.height))

class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Game")

        self.left_paddle = Paddle(10, (HEIGHT - PADDLE_HEIGHT) // 2)
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()
        
        self.left_paddle.limit_y()

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.left_paddle.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = PongGame()
    game.run()
