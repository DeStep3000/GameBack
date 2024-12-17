from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, Scrollbar, Frame, Toplevel, Label, messagebox, Entry

from sqlalchemy import create_engine, text

from configs.config_app_user import dbname, user, password, host, port

DATABASE_URL = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}'
engine = create_engine(DATABASE_URL)

ASSETS_PATH = Path(__file__).parent.parent / "build" / "assets" / "frame02"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class MainWindow(Frame):
    def __init__(self, parent, switch_to_login):
        super().__init__(parent)
        self.configure(bg="#EEE2DC")

        # Добавляем атрибут для хранения текущего ID игры
        self.current_game_id = None

        self.switch_to_login = switch_to_login

        self.main_canvas = Canvas(self, bg="#EEE2DC", height=668, width=1094, bd=0, highlightthickness=0,
                                  relief="ridge")
        self.main_canvas.grid(row=0, column=0, sticky="nsew")

        self.main_scrollbar = Scrollbar(self, orient="vertical", command=self.main_canvas.yview)
        self.main_scrollbar.grid(row=0, column=1, sticky="ns")

        self.main_canvas.config(yscrollcommand=self.main_scrollbar.set)

        self.content_frame = Frame(self.main_canvas, bg="#EEE2DC")
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>", self.on_frame_configure)

        # Верхняя панель (header)
        self.header = Frame(self.content_frame, bg="#EDC7B7", height=58)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")  # Stretch header across the width

        Label(self.header, text="Gameback", bg="#EDC7B7", fg="#AC3B61", font=("InknutAntiqua Regular", 40)).pack(
            side="left", padx=20)

        # Добавляем Label для отображения имени пользователя
        self.username_label = Label(
            self.header,
            text=f"Пользователь: {self.master.current_username}",
            bg="#EDC7B7",
            fg="#123C69",
            font=("Inter", 14)
        )
        self.username_label.pack(side="left", padx=10)

        self.button_logout = Button(
            self.header, text="Выход", bg="#AC3B61", fg="white",
            font=("Inter", 14), command=self.logout
        )
        self.button_logout.pack(side="right", padx=10)

        # Статичные кнопки сверху
        # Кнопка "Игры" (button_4)
        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        Button(
            self.header,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.master.show_frame('MainWindow'),  # Переключение на окно MainWindow
            relief="flat"
        ).pack(side="right", padx=5)

        # Кнопка "Мои отзывы" (button_5)
        self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        Button(
            self.header,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.master.show_frame('ProfileWindow'),  # Переключение на окно ProfileWindow
            relief="flat"
        ).pack(side="right", padx=5)

        # Left Panel
        self.left_frame = Frame(self.content_frame, bg="#EEE2DC", width=200)
        self.left_frame.grid(row=1, column=0, sticky="ns", padx=10, pady=10)

        # Right Panel
        self.right_frame = Frame(self.content_frame, bg="#BAB2B5")
        self.right_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Game Information
        self.game_title = Label(self.right_frame, text="", bg="#BAB2B5", fg="#123C69", font=("Inter", 18))
        self.game_title.pack(pady=10, padx=20, anchor="nw")

        self.game_description = Label(self.right_frame, text="", bg="#BAB2B5", fg="#123C69", font=("Inter", 14),
                                      wraplength=800, justify="left")
        self.game_description.pack(pady=5, padx=20, anchor="nw")

        self.game_details = Label(self.right_frame, text="", bg="#BAB2B5", fg="#123C69", font=("Inter", 14),
                                  wraplength=800, justify="left")
        self.game_details.pack(pady=5, padx=20, anchor="nw")

        self.reviews_label = Label(self.right_frame, text="Отзывы:", bg="#BAB2B5", fg="#123C69", font=("Inter", 16))
        self.reviews_label.pack(pady=10, padx=20, anchor="nw")

        self.reviews_container = Frame(self.right_frame, bg="#BAB2B5")
        self.reviews_container.pack(pady=5, padx=20, anchor="nw")

        self.create_game_buttons()

    def logout(self):
        self.master.current_user_id = None
        self.master.current_username = None
        self.switch_to_login()  # Возвращаемся на окно логина

    def refresh(self):
        """Обновляет имя пользователя в хедере"""
        self.username_label.config(text=f"Пользователь: {self.master.current_username}")

    def update_username(self):
        self.username_label.config(text=f"Пользователь: {self.master.current_username}")

    def create_game_buttons(self):
        # Получаем список игр из базы данных
        with engine.connect() as connection:
            result = connection.execute(text("SELECT GameID, Title FROM games.Games")).fetchall()

        self.games = {row[0]: row[1] for row in result}

        def on_game_button_click(game_id):
            self.current_game_id = game_id  # Обновляем текущий ID игры
            self.update_game_info(game_id)

        for game_id, title in self.games.items():
            button = Button(self.left_frame, text=title, bg="#AC3B61", fg="white", font=("Inter", 14),
                            command=lambda g_id=game_id: on_game_button_click(g_id))
            button.pack(pady=5, padx=10, anchor="w")

    def show_details(self):
        details_window = Toplevel(self)
        details_window.title("Подробнее")
        details_window.minsize(600, 500)
        details_window.configure(bg="#EEE2DC")
        # Позиционируем окно по центру экрана
        details_window.geometry("+%d+%d" % (self.winfo_rootx() + 50, self.winfo_rooty() + 50))

        # Контейнер для информации
        container = Frame(details_window, bg="#EEE2DC")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        with engine.connect() as connection:
            try:
                game_info = connection.execute(
                    text("SELECT * FROM games.get_game_info(:game_id)"),
                    {'game_id': self.current_game_id}  # Используем ID текущей игры
                ).mappings().fetchone()

                if game_info:
                    Label(details_window, text=f"Название: {game_info['title']}", font=("Inter", 16, "bold"),
                          bg="#EEE2DC", fg="#123C69").pack(pady=10, anchor="nw")
                    Label(details_window, text=f"Описание: {game_info['description']}", font=("Inter", 14),
                          bg="#EEE2DC", fg="#123C69", wraplength=500, justify="left").pack(pady=10, anchor="nw")
                    Label(details_window, text=f"Жанр: {game_info['genre']}", font=("Inter", 14), bg="#EEE2DC",
                          fg="#123C69").pack(pady=10, anchor="nw")
                    Label(details_window, text=f"Разработчик: {game_info['developer']}", font=("Inter", 14),
                          bg="#EEE2DC", fg="#123C69").pack(pady=10, anchor="nw")
                    Label(details_window, text=f"Страна: {game_info['country']}", font=("Inter", 14),
                          bg="#EEE2DC", fg="#123C69").pack(pady=10, anchor="nw")
                    Label(details_window, text=f"Средний рейтинг: {game_info['averagerating']:.1f}/10",
                          font=("Inter", 14), bg="#EEE2DC", fg="#123C69").pack(pady=10, anchor="nw")
                else:
                    Label(details_window, text="Информация об игре не найдена.", font=("Inter", 14),
                          bg="#EEE2DC", fg="#123C69").pack(pady=20)

            except Exception as e:
                Label(details_window, text=f"Ошибка: {e}", font=("Inter", 14), bg="#EEE2DC", fg="#123C69").pack(pady=20)

        # Автоматическое изменение размера окна под содержимое
        details_window.update_idletasks()  # Обновляет размеры всех виджетов
        width = container.winfo_reqwidth() + 20
        height = container.winfo_reqheight() + 20
        details_window.geometry(f"{width}x{height}")

    def leave_review(self):
        review_window = Toplevel(self)
        review_window.title("Оставить отзыв")
        review_window.geometry("500x400")
        review_window.configure(bg="#EEE2DC")

        Label(review_window, text="Ваш отзыв:", font=("Inter", 16), bg="#EEE2DC", fg="#123C69").pack(pady=10,
                                                                                                     anchor="w")

        # Поле ввода отзыва
        review_text = Entry(review_window, font=("Inter", 14), width=50)
        review_text.pack(pady=10, padx=20)

        Label(review_window, text="Ваша оценка:", font=("Inter", 16), bg="#EEE2DC", fg="#123C69").pack(pady=10,
                                                                                                       anchor="w")

        # Выбор оценки через звездочки
        rating_frame = Frame(review_window, bg="#EEE2DC")
        rating_frame.pack(pady=10)
        stars = []
        for i in range(1, 6):
            star_button = Button(rating_frame, text="☆", font=("Inter", 20), bg="#EEE2DC", fg="#AC3B61",
                                 command=lambda idx=i: set_rating(idx, stars))
            star_button.grid(row=0, column=i - 1, padx=5)
            stars.append(star_button)

        # Установка оценки
        selected_rating = [0]  # Храним выбранную оценку

        def set_rating(idx, stars):
            selected_rating[0] = idx * 2  # Преобразование в оценку от 1 до 10
            for star in stars:
                star.config(text="☆")
            for j in range(idx):
                stars[j].config(text="★")

        def submit_review():
            if selected_rating[0] == 0 or not review_text.get().strip():
                messagebox.showwarning("Предупреждение", "Заполните все поля и выберите оценку.")
                return

            user_id = self.master.current_user_id
            if not user_id:
                messagebox.showerror("Ошибка", "Не удалось определить текущего пользователя. Перезайдите в систему.")
                return

            with engine.connect() as connection:
                try:
                    # Вызов функции для проверки существующего отзыва
                    result = connection.execute(
                        text("SELECT users.check_review_exists(:game_id, :user_id)"),
                        {"game_id": self.current_game_id, "user_id": user_id}
                    ).scalar()

                    if result:  # Если функция вернула TRUE
                        messagebox.showwarning("Предупреждение", "Вы уже оставили отзыв для этой игры.")
                        return

                    # Если отзыва нет, добавляем его
                    connection.execute(
                        text("CALL users.add_review(:game_id, :user_id, :rating, :comment)"),
                        {
                            'game_id': self.current_game_id,
                            'user_id': user_id,
                            'rating': selected_rating[0],
                            'comment': review_text.get().strip()
                        }
                    )
                    connection.commit()
                    messagebox.showinfo("Успех", "Отзыв успешно добавлен!")
                    review_window.destroy()
                    self.update_game_info(self.current_game_id)
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось добавить отзыв: {e}")

        # Кнопка "Отправить"
        Button(review_window, text="Отправить", font=("Inter", 14), bg="#AC3B61", fg="white",
               command=submit_review).pack(pady=20)

    def update_game_info(self, game_id):
        self.current_game_id = game_id  # Устанавливаем текущую игру
        # Подключение к базе данных
        with engine.connect() as connection:
            try:
                game_info = connection.execute(
                    text("SELECT * FROM games.get_game_info(:game_id)"),
                    {'game_id': int(game_id)}
                ).mappings().fetchone()

                if game_info:
                    # Обновление названия игры с жирным шрифтом
                    self.game_title.config(text=game_info['title'], font=("Inter", 18, "bold"))
                    self.game_description.config(text=f"Описание: {game_info['description']}")

                    # Удаление старых кнопок и отзывов
                    for widget in self.right_frame.winfo_children():
                        if isinstance(widget, Button) or isinstance(widget,
                                                                    Label) and widget != self.game_title and widget != self.game_description:
                            widget.destroy()

                    # Кнопка "Подробнее"
                    self.button_details = Button(self.right_frame, text="Подробнее", bg="#AC3B61", fg="white",
                                                 font=("Inter", 14), command=self.show_details)
                    self.button_details.pack(pady=5, padx=20, anchor="w")

                    # Кнопка "Оставить отзыв"
                    self.button_review = Button(self.right_frame, text="Оставить отзыв", bg="#AC3B61", fg="white",
                                                font=("Inter", 14), command=self.leave_review)
                    self.button_review.pack(pady=5, padx=20, anchor="w")

                    # Отображение отзывов
                    reviews_label = Label(self.right_frame, text="Отзывы:", bg="#BAB2B5", fg="#123C69",
                                          font=("Inter", 16))
                    reviews_label.pack(pady=10, padx=20, anchor="nw")

                    # Получение отзывов
                    reviews = connection.execute(
                        text("SELECT * FROM games.get_reviews_for_game(:game_id)"),
                        {'game_id': int(game_id)}  # Приведение game_id к int
                    ).mappings().fetchall()  # Преобразование результата в словарь

                    # Обновление отзывов
                    if reviews:
                        for review in reviews:
                            Label(self.right_frame,
                                  text=f"{review['username']} ({review['rating']}/10): {review['comment']}",
                                  bg="#BAB2B5",
                                  fg="#123C69", font=("Inter", 14), wraplength=800, justify="left").pack(pady=5,
                                                                                                         padx=20,
                                                                                                         anchor="nw")
                    else:
                        Label(self.right_frame, text="Отзывов пока нет.", bg="#BAB2B5", fg="#123C69",
                              font=("Inter", 14),
                              wraplength=800, justify="left").pack(pady=5, padx=20, anchor="nw")

                else:
                    messagebox.showinfo("Информация", "Информация об игре не найдена.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось получить информацию об игре: {e}")

    def on_frame_configure(self, event):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
