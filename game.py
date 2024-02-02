import pygame
import random
import math
import matplotlib.pyplot as plt
import numpy as np

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
    def __init__(self, posx, posy, width, height, speed, color, learning_rate=0.9, discount_factor=0.5, epsilon=0.9):
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
        #obliczanie środka paletki
        center_posy = self.posy + self.height // 2
        current_state = (center_posy, round(ball.posy / 10) * 10)
        

        # Wybierz akcję zgodnie z algorytmem Q-learning
        action = self._choose_action(current_state)

        # Oblicz nową pozycję, ale jeszcze jej nie przypisuj
        new_center_posy = center_posy + self.speed * action

        # Sprawdź, czy nowa pozycja nie wyjdzie poza górny lub dolny kraniec ekranu
        if new_center_posy - self.height // 2 < 0:
            new_center_posy = self.height // 2
        elif new_center_posy + self.height // 2 > HEIGHT:
            new_center_posy = HEIGHT - self.height // 2

        # Teraz przypisz obliczoną pozycję, która jest już skorygowana
        self.posy = new_center_posy - self.height // 2

        # Dostosuj funkcję nagrody w zależności od odbicia piłki
        point = ball.update()
        reward = self._calculate_reward(ball, point)

        
        # Oblicz nową wartość Q dla aktualnego stanu i akcji
        new_state = (center_posy, round(ball.posy / 10) * 10)
        self._update_q_value(current_state, action, reward, new_state)

        # Aktualizuj rect
        self.geekRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

        return current_state, action, new_state

    def _choose_action(self, state):
         # Sprawdź czy dany stan jest w tabeli Q, w przeciwnym razie wybierz losową akcję
        if state not in self.q_table or random.uniform(0, 1) < self.epsilon:
            # Epsilon-greedy eksploracja
            action = random.choice([-1, 0, 1])
        else:
            # Podejmij decyzję na podstawie wartości Q z tabeli
            action = max(self.q_table[state], key=self.q_table[state].get, default=0)

        return action

    def update_epsilon(self):
        # Zmniejszanie epsilon w czasie
        self.epsilon = max(0.1, self.epsilon * 0.9999)
        
    def _calculate_reward(self, ball, point):
        # Maksymalna akceptowalna odległość
        max_distance = 100 

        # Oblicz odległość między paletką a piłką
        distance_to_ball = abs(ball.posy - (self.posy + self.height // 2))
        # Kara za oddalanie się od piłki
        penalty = 0.01

        # Oblicz nagrodę z uwzględnieniem kary
        reward = max(0, 1 - distance_to_ball / max_distance) - penalty

    
       

        return reward

    def _update_q_value(self, state, action, reward, new_state):
        # Parametry uczenia
        learning_rate = self.learning_rate
        discount_factor = self.discount_factor

        # Inicjalizacja wartości Q jeśli stan nie jest w tabeli Q
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in [-1, 0, 1]}
        if new_state not in self.q_table:
            self.q_table[new_state] = {a: 0 for a in [-1, 0, 1]}

        # Oblicz zaktualizowaną wartość Q
        old_q_value = self.q_table[state][action]
        max_future_q = max(self.q_table[new_state].values())
        new_q_value = old_q_value + learning_rate * (reward + discount_factor * max_future_q - old_q_value)

        # Zaktualizuj wartość Q
        self.q_table[state][action] = new_q_value

# Klasa paletki
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        # Rect kontrolujące kolizję i pozycję paletki
        self.geekRect = pygame.Rect(posx, posy, width, height)
        # Renderowanie obiektu
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    # Wyświetlanie obiektu
    def display(self):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, yFac=None):
        if yFac is not None:
            self.posy = self.posy + self.speed * yFac

        # Nadawanie ogranieczeń związanych z rozmiarem mapy
        if self.posy <= 0:
            self.posy = 0
        
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

        # Aktualizacja rect o nowe wartości
        self.geekRect = (self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    def getRect(self):
        return self.geekRect
#zliczanie stanów
def count_states(q_table):
    return len(q_table)
#Tabela dla jednego wybranego stanu
def print_q_table(q_table, state):
    print(f"+---------------------+-----+-----+-----+")
    print(f"|      Stan/Akcja     |  -1 |  0  |  1  |")
    print(f"+---------------------+-----+-----+-----+")

    if state in q_table:
        actions = q_table[state]
        state_str = f"| ({state[0]}, {state[1]})".ljust(21)
        action_str = f"| {actions[-1]:.2f} | {actions[0]:.2f} | {actions[1]:.2f} |"
        print(state_str + action_str)
    else:
        print(f"| ({state[0]}, {state[1]}) not found in Q-table".ljust(41) + "|")

    print(f"+---------------------+-----+-----+-----+")

# Klasa piłki
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

def print_final_q_table(q_table):
    print("\nFinal Q-table:")
    print(f"+---------------------+-----+-----+-----+")
    print(f"|      Stan/Akcja     |  -1 |  0  |  1  |")
    print(f"+---------------------+-----+-----+-----+")

    for state, actions in q_table.items():
        state_str = f"| ({state[0]}, {state[1]})".ljust(21)
        action_str = f"| {actions[-1]:.2f} | {actions[0]:.2f} | {actions[1]:.2f} |"
        print(state_str + action_str)

    print(f"+---------------------+-----+-----+-----+")
# Game Manager
def main():
    running = True

    # Defining the objects
    geek1 = Striker(20, 0, 10, 100, 10, GREEN)
    geek2 = LearningStriker(WIDTH - 30, HEIGHT // 2, 10, 100, 20, GREEN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 2, WHITE)

    listOfGeeks = [geek1, geek2]

    # Initial parameters of the players
    geek1Score, geek2Score = 0, 0
    frame_counter = 0
    while running:
        screen.fill(BLACK)

        # Detekcja kolizji
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
        # Aktualizacja obiektów
        geek1.update()
        if frame_counter % 1 == 0:
            current_state, action, new_state = geek2.update(ball)
            geek2.update_epsilon()
            
        if frame_counter % FPS == 0:
            # Wypisz tabelkę Q akcje co zostalo wybrane
            print("Current state:", current_state, "Action:", action, "New state:", new_state)
            print_q_table(geek2.q_table, current_state)
            num_states = count_states(geek2.q_table)
            print("Liczba stanów w tabeli Q:", num_states)
            print("Epsilon wynosi: ", geek2.epsilon)
        frame_counter += 1
        point = ball.update()

        # -1 -> Geek_1 zdobył punkt
        # +1 -> Geek_2 zdobył punkt
        #  0 -> Nikt nie zdobył punktu
        if point == -1:
            geek1Score += 1
        elif point == 1:
            geek2Score += 1

        # Reset piłki po zdobyciu punktu
        if point:
            ball.reset()

        # Wyświetlanie obiektów
        geek1.display()
        geek2.display()
        ball.display()

        # Wyswietlanie punktacji
        geek1.displayScore("Geek_1 : ",
                           geek1Score, 100, 20, WHITE)
        geek2.displayScore("Geek_2 : ",
                           geek2Score, WIDTH - 100, 20, WHITE)

        pygame.display.update()
        clock.tick(FPS)
    #Wyświetlanie końcowej tabeli stanów
    print_final_q_table(geek2.q_table)

if __name__ == "__main__":
    main()
    pygame.quit()
