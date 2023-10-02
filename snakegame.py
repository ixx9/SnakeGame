import pygame
import time
import random

def end_game(screen, score, music):
    music.stop()
    font = pygame.font.SysFont('Arial', 30)
    text = 'Вы набрали ' + str(score) + ' очков!'
    text1 = 'Для перезапуска игры нажмите пробел'
    text_surf = font.render(text, True, (255, 255, 255))
    text_surf1 = font.render(text1, True, (255, 255, 255))
    screen.blit(text_surf, (250, 220))
    screen.blit(text_surf1, (150, 260))
    pygame.display.flip()

running = True
while running:
    # Инициализация Pygame
    pygame.init()

    # Настройка экрана
    width, height = 740, 580
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Змейка")

    # Музыка
    music = pygame.mixer.Sound('music/music.mp3')
    music.play(-1)
    music.set_volume(0.1)


    # Цвета
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)

    # Изображения
    field = pygame.image.load('img/field.png')
    field = pygame.transform.scale(field, (740, 580))

    apple = pygame.image.load('img/apple.png')
    apple = pygame.transform.scale(apple, (20, 20))

    snake = pygame.image.load('img/snake.png')
    snake = pygame.transform.scale(snake, (20, 20))

    # Задержка обновления экрана
    fps = pygame.time.Clock()

    # Настройка переменных игры
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, width // 20) * 20, random.randrange(1, height // 20) * 20]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    # Функция отображения счета на экране
    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Счет : ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        screen.blit(score_surface, score_rect)

    # Основной цикл игры
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        # Обновление направления движения
        direction = change_to

        # Изменение координат змейки
        if direction == 'UP':
            snake_pos[1] -= 20
        if direction == 'DOWN':
            snake_pos[1] += 20
        if direction == 'LEFT':
            snake_pos[0] -= 20
        if direction == 'RIGHT':
            snake_pos[0] += 20

        # Увеличение длины змейки
        snake_body.insert(0, list(snake_pos))
        if pygame.Rect(snake_pos[0], snake_pos[1], 20, 20).colliderect(pygame.Rect(food_pos[0], food_pos[1], 20, 20)):
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            eat = pygame.mixer.Sound('music/eat.mp3')
            eat.play()
            eat.set_volume(0.3)
            food_pos = [random.randrange(1, width // 20) * 20, random.randrange(1, height // 20) * 20]
        food_spawn = True

        # Отрисовка элементов игры
        screen.blit(field, (0, 0))

        for pos in snake_body:
            screen.blit(snake, (pos[0], pos[1], 20, 20))
        screen.blit(apple, (food_pos[0], food_pos[1]))


        # Завершение игры при столкновении со стенами или с собственным телом
        if snake_pos[0] < 0 or snake_pos[0] > width - 20:
            game_over = True
        if snake_pos[1] < 0 or snake_pos[1] > height - 20:
            game_over = True
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over = True

        # Отображение счета
        show_score(1, white, 'consolas', 20)

        # Обновление экрана
        pygame.display.update()

        # Задержка обновления экрана
        fps.tick(10)

    # Запуск функции окончания игры
    end_game(screen, score, music)

    # Ожидание перезапуска игры
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Выход из игры
pygame.quit()
quit()