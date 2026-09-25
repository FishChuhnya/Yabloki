import tkinter as tk
import random

# --- УРОВЕНЬ 1: Изменяем настройки окна и игры ---
root = tk.Tk()
root.title("Ультра Сборщик: Время Напрячься!")  # Новое название игры

WIDTH = 600  # Новый размер игрового окна
HEIGHT = 600

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT
)
canvas.pack()

# --- УРОВЕНЬ 2: Загрузка картинок через tk.PhotoImage ---
# Убедитесь, что файлы лежат в папке img/ рядом с вашим скриптом!
bg_image = tk.PhotoImage(file="img/tree.png")
basket_image = tk.PhotoImage(file="img/basket.png")
apple_image = tk.PhotoImage(file="img/apple.png")
pear_image = tk.PhotoImage(file="img/pear.png")
bomb_image = tk.PhotoImage(file="img/bomb.png")
trash_image = tk.PhotoImage(file="img/can.png")

# Отрисовка фона
bg_id = canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Счёт и УРОВЕНЬ 4: Таймер вместо жизней
score = 0
time_left = 30  # Ровно 30 секунд на игру
game_active = True

score_text = canvas.create_text(
    60,
    20,
    text="Счёт: 0",
    font=("Arial", 16, "bold"),
    fill="white"
)

# УРОВЕНЬ 4: Текст таймера в верхней части экрана
timer_text = canvas.create_text(
    WIDTH - 80,
    20,
    text="Время: 30с",
    font=("Arial", 16, "bold"),
    fill="red"
)

# Корзинка (Заменена на картинку по Уровню 2)
basket_x = WIDTH // 2
basket_y = HEIGHT - 60

basket = canvas.create_image(
    basket_x,
    basket_y,
    image=basket_image
)

# Падающие предметы
objects = []


# Создание предметов
def create_object():
    if not game_active:
        return

    # Подстраиваем спавн под новые размеры окна
    x = random.randint(40, WIDTH - 40)
    y = 0

    # УРОВЕНЬ 2 и 4: Разделение на 4 типа предметов с разным шансом
    rand_num = random.randint(1, 10)

    if rand_num <= 5:  # 50% шанс — Яблоко
        item = canvas.create_image(x, y, image=apple_image)
        object_type = "apple"
    elif rand_num <= 7:  # 20% шанс — Груша (+2 очка)
        item = canvas.create_image(x, y, image=pear_image)
        object_type = "pear"
    elif rand_num <= 9:  # 20% шанс — Банка/Мусор (-1 очко)
        item = canvas.create_image(x, y, image=trash_image)
        object_type = "trash"
    else:  # 10% шанс — Опасная бомба (-2 очка)
        item = canvas.create_image(x, y, image=bomb_image)
        object_type = "bomb"

    objects.append([item, x, y, object_type])

    # УРОВЕНЬ 3: Время между появлением предметов уменьшается с ростом счёта
    # Стартуем с 1000мс, уменьшаем на каждые 15мс за очко, но не быстрее 400мс
    current_delay = max(400, 1000 - (score * 15))
    root.after(current_delay, create_object)


# Движение корзинки (с учётом новых границ окна 600px)
def move_left(event):
    global basket_x
    if game_active and basket_x > 50:
        basket_x -= 25
        canvas.coords(basket, basket_x, basket_y)


def move_right(event):
    global basket_x
    if game_active and basket_x < WIDTH - 50:
        basket_x += 25
        canvas.coords(basket, basket_x, basket_y)


# УРОВЕНЬ 4: Каждую секунду уменьшаем таймер
def update_timer():
    global time_left, game_active
    if not game_active:
        return

    time_left -= 1
    canvas.itemconfig(timer_text, text=f"Время: {time_left}с")

    if time_left <= 0:
        game_active = False
        end_game()
    else:
        root.after(1000, update_timer)


# Игровой цикл
def update_game():
    global score

    if not game_active:
        return

    # УРОВЕНЬ 1 и УРОВЕНЬ 3: Базовая скорость падения увеличена,
    # плюс скорость растёт на 1 единицу за каждые 5 набранных очков
    current_speed = 6 + (score // 5)

    for obj in objects[:]:
        item = obj[0]
        x = obj[1]
        y = obj[2]
        object_type = obj[3]

        # Двигаем предмет вниз с динамической скоростью
        y += current_speed
        obj[2] = y

        canvas.move(item, 0, current_speed)

        # Проверяем, поймали ли предмет корзиной (высота basket_y = HEIGHT - 60)
        if y >= HEIGHT - 90 and y <= HEIGHT - 40:
            if abs(x - basket_x) < 50:  # Ширина ловли под картинку

                # УРОВЕНЬ 4: Новые правила набора очков
                if object_type == "apple":
                    score += 1
                elif object_type == "pear":
                    score += 2
                elif object_type == "trash":
                    score -= 1
                elif object_type == "bomb":
                    score -= 2

                canvas.itemconfig(score_text, text=f"Счёт: {score}")
                canvas.delete(item)
                objects.remove(obj)
                continue

        # Если предмет упал мимо экрана (в режиме на время за пропуск ничего не отнимается)
        if y > HEIGHT:
            canvas.delete(item)
            objects.remove(obj)

    if game_active:
        root.after(30, update_game)


# Конец игры
def end_game():
    canvas.delete("all")

    # Снова рисуем фон на чистом экране
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    # УРОВЕНЬ 1 и УРОВЕНЬ 4: Полностью переписанный текст окончания игры
    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
        text=f"Время вышло!\nТы набрал {score} очков.",
        font=("Arial", 28, "bold"),
        fill="black",
        justify="center"
    )


# Управление
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

# Запуск игры
create_object()
update_game()
update_timer()  # Запуск отсчета 30 секунд

root.mainloop()