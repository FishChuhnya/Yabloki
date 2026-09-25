import tkinter as tk
import random
import os

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

# --- ФУНКЦИЯ БЕЗОПАСНОЙ ЗАГРУЗКИ КАРТИНОК ---
# Если картинки нет, возвращает False, и игра нарисует красивую фигуру-заглушку.
def load_image(path):
    if os.path.exists(path):
        try:
            return tk.PhotoImage(file=path)
        except Exception:
            return None
    return None

# Пытаемся загрузить картинки
bg_image = load_image("img/tree.png")
basket_image = load_image("img/basket.png")
apple_image = load_image("img/apple.png")
pear_image = load_image("img/pear.png")
bomb_image = load_image("img/bomb.png")
trash_image = load_image("img/can.png")

# Отрисовка фона (если картинки нет — будет тёмно-зелёный фон)
if bg_image:
    bg_id = canvas.create_image(0, 0, image=bg_image, anchor="nw")
else:
    bg_id = canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#2e5c1e", outline="")

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

# Корзинка (Заменена на картинку по Уровню 2 / фигуру при отсутствии)
basket_x = WIDTH // 2
basket_y = HEIGHT - 60

if basket_image:
    basket = canvas.create_image(basket_x, basket_y, image=basket_image)
else:
    # Если картинки нет — рисуем коричневую корзину прямоугольником
    basket = canvas.create_rectangle(basket_x - 40, basket_y - 20, basket_x + 40, basket_y + 20, fill="#8B4513", outline="white", width=2)

# Падающие предметы
objects = []

# Вспомогательная функция создания предмета (картинка или цветной кружок)
def draw_falling_item(x, y, img, backup_color):
    if img:
        return canvas.create_image(x, y, image=img)
    else:
        # Если картинки нет — рисуем круг радиусом 15 пикселей
        return canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=backup_color, outline="white")

# Создание предметов
def create_object():
    if not game_active:
        return

    x = random.randint(40, WIDTH - 40)
    y = 30

    # УРОВЕНЬ 2 и 4: Разделение на 4 типа предметов с разным шансом
    rand_num = random.randint(1, 10)

    if rand_num <= 5:  # 50% шанс — Яблоко (Красное)
        item = draw_falling_item(x, y, apple_image, "red")
        object_type = "apple"
    elif rand_num <= 7:  # 20% шанс — Груша (Жёлтая)
        item = draw_falling_item(x, y, pear_image, "yellow")
        object_type = "pear"
    elif rand_num <= 9:  # 20% шанс — Банка/Мусор (Серый)
        item = draw_falling_item(x, y, trash_image, "gray")
        object_type = "trash"
    else:  # 10% шанс — Опасная бомба (Чёрная)
        item = draw_falling_item(x, y, bomb_image, "black")
        object_type = "bomb"

    objects.append([item, x, y, object_type])

    # УРОВЕНЬ 3: Время между появлением предметов уменьшается с ростом счёта
    current_delay = max(400, 1000 - (score * 15))
    root.after(current_delay, create_object)


# Движение корзинки
def move_left(event):
    global basket_x
    if game_active and basket_x > 50:
        basket_x -= 25
        if basket_image:
            canvas.coords(basket, basket_x, basket_y)
        else:
            canvas.coords(basket, basket_x - 40, basket_y - 20, basket_x + 40, basket_y + 20)


def move_right(event):
    global basket_x
    if game_active and basket_x < WIDTH - 50:
        basket_x += 25
        if basket_image:
            canvas.coords(basket, basket_x, basket_y)
        else:
            canvas.coords(basket, basket_x - 40, basket_y - 20, basket_x + 40, basket_y + 20)


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

    current_speed = 6 + (score // 5)

    for obj in objects[:]:
        item = obj[0]
        x = obj[1]
        y = obj[2]
        object_type = obj[3]

        y += current_speed
        obj[2] = y

        canvas.move(item, 0, current_speed)

        # Проверяем ловлю корзиной
        if y >= HEIGHT - 90 and y <= HEIGHT - 40:
            if abs(x - basket_x) < 50:

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

        # Если предмет упал мимо экрана
        if y > HEIGHT + 20:
            canvas.delete(item)
            objects.remove(obj)

    if game_active:
        root.after(30, update_game)


# Конец игры
def end_game():
    canvas.delete("all")

    # Снова рисуем фон или заливку
    if bg_image:
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
    else:
        canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#2e5c1e", outline="")

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
        text=f"Время вышло!\nТы набрал {score} очков.",
        font=("Arial", 28, "bold"),
        fill="white" if not bg_image else "black",
        justify="center"
    )


# Управление
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

# Запуск игры
create_object()
update_game()
update_timer()

root.mainloop()
