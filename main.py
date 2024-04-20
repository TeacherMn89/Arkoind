import pygame  # Імпортуємо бібліотеку pygame
pygame.init()  # Ініціалізуємо pygame

back = (200, 255, 255)  # Встановлюємо колір фону
mw = pygame.display.set_mode((500, 500))  # Створюємо головне вікно
mw.fill(back)  # Заповнюємо головне вікно фоновим кольором
clock = pygame.time.Clock()  # Створюємо годинник для регулювання швидкості гри
dx = 1  # Задаємо початкову швидкість руху м'яча по осі X
dy = 1  # Задаємо початкову швидкість руху м'яча по осі Y

platform_x = 200  # Визначаємо початкове положення платформи по осі X
platform_y = 330  # Визначаємо початкове положення платформи по осі Y
move_right = False  # Прапорець для руху платформи вправо
move_left = False  # Прапорець для руху платформи вліво
game_over = False  # Прапорець для визначення закінчення гри

# Клас для визначення області екрану
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        # Ініціалізація області з параметрами за замовчуванням
        self.rect = pygame.Rect(x, y, width, height)
        # Встановлення кольору за замовчуванням або вказаного
        self.fill_color = back if color is None else color

    def color(self, new_color):
        # Зміна кольору області
        self.fill_color = new_color

    def fill(self):
        # Заповнення області встановленим кольором
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        # Перевірка чи точка (x, y) знаходиться всередині області
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        # Перевірка колізії із заданим прямокутником
        return self.rect.colliderect(rect)

# Клас для визначення текстової мітки
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        # Створення тексту з вказаним розміром та кольором
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        # Заповнення області та виведення текстового зображення зі зсувом
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

# Клас для визначення зображення
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        # Ініціалізація зображення з параметрами за замовчуванням
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        # Завантаження зображення із заданим ім'ям файлу
        self.image = pygame.image.load(filename)

    def draw(self):
        # Виведення зображення на екран у вказаних координатах
        mw.blit(self.image, (self.rect.x, self.rect.y))

# Створення об'єктів гри
ball = Picture('ball3.png', 160, 200, 50, 50)  # Створюємо об'єкт м'яча
platform = Picture('platform.png', platform_x, platform_y, 100, 30)  # Створюємо об'єкт платформи
start_x = 5  # Визначаємо початкове положення початкового монстра по осі X
start_y = 5  # Визначаємо початкове положення початкового монстра по осі Y
count = 9  # Визначаємо початкову кількість монстрів в ряду

monsters = []  # Створюємо порожній список для зберігання монстрів
for j in range(3):
    y = start_y + (55 * j)
    x = start_x + (27.5 * j)
    for i in range(count):
        d = Picture('enemy.png', x, y, 50, 50)  # Створюємо об'єкт монстра
        monsters.append(d)  # Додаємо монстра до списку
        x = x + 55
    count = count - 1

# Головний цикл гри, в якому відбувається відображення та обробка подій
while not game_over:
    # Заповнюємо області м'яча та платформи фоновим кольором
    ball.fill()
    platform.fill()

    # Обробка подій (натискання та відпускання клавіш, вихід з гри)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False

    # Переміщення платформи та м'яча
    if platform.rect.x < 0:
        platform.rect.x += 3

    if move_right:
        platform.rect.x += 3
    if move_left:
        platform.rect.x -= 3
    ball.rect.x += dx
    ball.rect.y += dy

    # Логіка відбиття м'яча від верхньої та бокових стінок
    if ball.rect.y < 0:
        dy *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1

    # Гравець програв, якщо м'яч впав за нижню межу вікна
    if ball.rect.y > 350:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text('YOU LOSE', 60, (255, 0, 0))
        time_text.draw(10, 10)
        game_over = True

    # Гравець виграв, якщо всі монстри знищені
    if len(monsters) == 0:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text('YOU WIN', 60, (0, 200, 0))
        time_text.draw(10, 10)
        game_over = True

    # Логіка відбиття м'яча від платформи та знищення монстрів
    if ball.rect.colliderect(platform.rect):
        dy *= -1
    for m in monsters:
        m.draw()
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            dy *= -1

    # Відображення платформи та м'яча на екрані
    platform.draw()
    ball.draw()

    # Оновлення екрану та регулювання швидкості гри
    pygame.display.update()
    clock.tick(60)
