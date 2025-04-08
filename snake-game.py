import pygame
import time
import random

pygame.init()

# Параметры экрана
a = 20
b = 20
screen_width, screen_height = a * 32, b * 32
screen = pygame.display.set_mode((screen_width, screen_height))

# Цвета
white = (255, 255, 255)
green = (0, 255, 0)
grey = (128, 128, 128)
red = (255, 0, 0)
black = (0, 0, 0)
pygame.display.set_caption("Змейка")

font = pygame.font.Font(None, 50)

# Класс для персонажа
class Character:
    def __init__(self, speed, x, y):
        self.x = x  # Координаты змейки по X
        self.y = y  # Координаты змейки по Y
        self.speed = speed  # Скорость змейки (интервал времени между движениями)

    def move(self, left, right, up, down):
        global a, b, food, isfood, buttonis, score
        food = False
        buttonis = False
        # Движение влево
        if left:
            self.x.append(self.x[-1] - 1)
            self.y.append(self.y[-1])
        # Движение вправо
        elif right:
            self.x.append(self.x[-1] + 1)
            self.y.append(self.y[-1])
        # Движение вверх
        elif up:
            self.x.append(self.x[-1])
            self.y.append(self.y[-1] - 1)
        # Движение вниз
        elif down:
            self.x.append(self.x[-1])
            self.y.append(self.y[-1] + 1)
        if self.x[-1] == xfood and self.y[-1] == yfood:
            food = True
        for i in range(len(self.x) - 1):
            if self.x[-1] == self.x[i] and self.y[-1] == self.y[i]:
                death()
        # Если еда не съедена, убираем хвост
        if not food:
            self.x.pop(0)
            self.y.pop(0)
        elif food:
            score += 1
            isfood = False
            player.spawnfood()
        

    def draw(self, screen):
        for i in range(len(self.x)):
            pygame.draw.rect(screen, green, (self.x[i] * 32, self.y[i] * 32, 32, 32))

    def spawnfood(self):
        global isfood, a, b, xfood, yfood
        if not isfood:
            xfood = random.randint(1,a-2)
            yfood = random.randint(1,b-2)
            for i in range(len(self.x)):
                if xfood == self.x[i] and yfood == self.y[i]:
                    player.spawnfood()
            isfood = True
        if isfood:
            pygame.draw.rect(screen, red, (xfood * 32, yfood * 32, 32, 32))
    


running = True
clock = pygame.time.Clock()
speed = 3
score = 0
record = 0
def death():
    global player, start, right, left, up, down, last_move_time, move_interval, isfood, speed, buttonis, score
    player = Character(speed, [2, 3, 4], [2, 2, 2])  # Змейка из трёх блоков
    start, right, left, up, down, isfood, buttonis  = False, False, False, False, False, False, False
    last_move_time, score = 0 , 0 # Сброс времени последнего движения
    move_interval = 250 - player.speed * 50



death()

# Основной игровой цикл
while running:
    current_time = pygame.time.get_ticks()  # Текущее время в миллисекундах

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if player.x[-1] == 0 or player.x[-1] == a - 1 or player.y[-1] == 0 or player.y[-1] == b - 1:
            death()
    
    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not right and not buttonis:  # Запрещаем поворот на 180 градусов
        right, left, up, down = False, True, False, False
        buttonis = True
    if keys[pygame.K_RIGHT] and not left and not buttonis:
        right, left, up, down = True, False, False, False
        buttonis = True
    if keys[pygame.K_UP] and not down and not buttonis:
        right, left, up, down = False, False, True, False
        buttonis = True
    if keys[pygame.K_DOWN] and not up and not buttonis:
        right, left, up, down = False, False, False, True
        buttonis = True
    if keys[pygame.K_SPACE]:
        if not start:
            start, right, left, up, down = True, True, False, False, False

    # Очистка экрана
    screen.fill(grey)
    pygame.draw.rect(screen, white, (32, 32, screen_width - 64, screen_height - 64))  # Поле игры

    if start:
        player.spawnfood()

    # Отрисовка змейки
    if record < score:
        record = score
    player.draw(screen)
    text_surface = font.render('score: ' + str(score) + '  record: ' + str(record), True, black)

    screen.blit(text_surface, (0,0))

    if not start:
        text_start = font.render('press SPACE to start the game', True, black)
        text_rect = text_start.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_start, text_rect)
    # Движение змейки по таймеру
    if start and current_time - last_move_time > move_interval:
        player.move(left, right, up, down)
        last_move_time = current_time  # Обновление времени последнего движения

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)  # Ограничение FPS

pygame.quit()
