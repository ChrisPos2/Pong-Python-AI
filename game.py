import pygame
import random
import math

pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 60

class LearningStriker:
    def __init__(self, posx, posy, width, height, speed, color, learning_rate=0.1, discount_factor=0.9, epsilon=0.9):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.epsilon = epsilon
        self.geekRect = pygame.Rect(posx, posy, width, height)
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        # Q-table dla każdego stanu i akcji
        self.q_table = {}

    def display(self):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)

    def getRect(self):
        return pygame.Rect(self.posx, self.posy, self.width, self.height)

    def update(self, ball):
        current_state = self.posy
        ball_x, ball_y = ball.posx, ball.posy

        # Wybierz akcję zgodnie z algorytmem Q-learning
        action = self._choose_action(current_state)

        # Przesuń gracza zgodnie z wybraną akcją
        self.posy += self.speed * action

        # Sprawdź, czy gracz nie wyjechał poza ekran
        if self.posy < 0:
            self.posy = 0
        elif self.posy + self.height > HEIGHT:
            self.posy = HEIGHT - self.height

        # Dostosuj funkcję nagrody w zależności od odbicia piłki
        point = ball.update()
        reward = self._calculate_reward(ball, point)

        # Oblicz nową wartość Q dla aktualnego stanu i akcji
        new_state = self.posy
        self._update_q_value(current_state, action, reward, new_state)

        # Aktualizuj rect
        self.geekRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

        return current_state, action, new_state

    def _choose_action(self, state):
        # Wybierz akcję zgodnie z algorytmem Q-learning lub losowo
        if state not in self.q_table or random.uniform(0, 1) < self.epsilon:  # Epsilon-greedy exploration
            action = random.choice([-1, 0, 1])
            print("Wybrano losową akcję:", action)
        else:
            action = max([-1, 0, 1], key=lambda a: self.q_table[state].get(a, 0))
            print("Wybrano akcję na podstawie tabeli Q:", action)
            print("Ilość danych w tabeli Q dla stanu", state, ":", len(self.q_table[state]))

        return action

    def update_epsilon(self):
        # Zmniejszanie epsilon w czasie
        self.epsilon = max(0.1, self.epsilon * 0.99999)
        print("Aktualna wartosc epsilon: ",self.epsilon)

    def _calculate_reward(self, ball, point):
        if pygame.Rect.colliderect(ball.getRect(), self.getRect()):
            # Nagroda za odbicie piłki
            reward = 1.0
            print("Piłka została odbita")
        else:
            # Kara za utratę punktu
            reward = -1.0 if point != 0 else 0.0

        print("Reward:", reward)  # Dodaj to, aby sprawdzić, jakie nagrody są przyznawane

        return reward

    def _update_q_value(self, state, action, reward, new_state):
        # Aktualizuj wartość Q za pomocą wzoru Q-learningu
        if state not in self.q_table:
            self.q_table[state] = {}

        if new_state not in self.q_table:
            self.q_table[new_state] = {}

        old_q_value = self.q_table[state].get(action, 0)
        max_future_q = max(self.q_table[new_state].values(), default=0)

        new_q_value = (1 - self.learning_rate) * old_q_value + self.learning_rate * (
                reward + self.discount_factor * max_future_q)

        self.q_table[state][action] = new_q_value


# Striker class
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        # Rect that is used to control the position and collision of the object
        self.geekRect = pygame.Rect(posx, posy, width, height)
        # Object that is blit on the screen
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    # Used to display the object on the screen
    def display(self):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, yFac=None):
        if yFac is not None:
            self.posy = self.posy + self.speed * yFac

        # Restricting the striker to be below the top surface of the screen
        if self.posy <= 0:
            self.posy = 0
        # Restricting the striker to be above the bottom surface of the screen
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

        # Updating the rect with the new values
        self.geekRect = (self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    def getRect(self):
        return self.geekRect


# Ball class
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        # If the ball hits the top or bottom surfaces,
        # then the sign of yFac is changed and
        # it results in a reflection
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= 0 and self.firstTime:
            self.reset()
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.reset()
            return -1
        else:
            return 0

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        # Losowy kąt odbicia w zakresie od -45 do 45 stopni
        self.angle = random.uniform(-45, 45)
        # Przelicz współczynniki xFac i yFac na podstawie kąta
        self.xFac = 1 if random.choice([True, False]) else -1
        self.yFac = 1 if random.choice([True, False]) else -1
        self.firstTime = 1

    # Used to reflect the ball along the X-axis
    def hit(self):
        self.xFac *= -1

    def getRect(self):
        return self.ball


# Game Manager
def main():
    running = True

    # Defining the objects
    geek1 = Striker(20, 0, 10, 100, 10, GREEN)
    geek2 = LearningStriker(WIDTH - 30, 0, 10, 100, 10, GREEN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 2, WHITE)

    listOfGeeks = [geek1, geek2]

    # Initial parameters of the players
    geek1Score, geek2Score = 0, 0
    geek1YFac, geek2YFac = 0, 0
    frame_counter = 0
    while running:
        screen.fill(BLACK)
        reward = 0
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    geek2YFac = -1
                if event.key == pygame.K_DOWN:
                    geek2YFac = 1
                if event.key == pygame.K_w:
                    geek1YFac = -1
                if event.key == pygame.K_s:
                    geek1YFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    geek2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    geek1YFac = 0

        # Collision detection
        for geek in listOfGeeks:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()
                # Po odbiciu od paletki, ustaw nowy losowy kąt odbicia
                ball.angle = random.uniform(-45, 45)
                # Przelicz współczynnik yFac na podstawie nowego kąta
                ball.yFac = round(math.sin(math.radians(ball.angle)), 2)
                # Losowanie prędkości piłki po odbiciu
                ball.speed = random.uniform(2, 4)

        geek1.posy = ball.posy - geek1.height / 2
        # Updating the objects
        geek1.update()
        if frame_counter % 1 == 0:
            current_state, action, new_state = geek2.update(ball)
            geek2.update_epsilon()
            print("Current state:", current_state, "Action:", action, "New state:", new_state)
        frame_counter += 1
        point = ball.update()

        # -1 -> Geek_1 has scored
        # +1 -> Geek_2 has scored
        #  0 -> None of them scored
        if point == -1:
            geek1Score += 1
        elif point == 1:
            geek2Score += 1

        # Someone has scored
        # a point and the ball is out of bounds.
        # So, we reset its position
        if point:
            ball.reset()

        # Displaying the objects on the screen
        geek1.display()
        geek2.display()
        ball.display()

        # Displaying the scores of the players
        geek1.displayScore("Geek_1 : ",
                           geek1Score, 100, 20, WHITE)
        geek2.displayScore("Geek_2 : ",
                           geek2Score, WIDTH - 100, 20, WHITE)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()
