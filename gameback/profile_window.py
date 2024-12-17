from pathlib import Path
from tkinter import Frame, Label, Entry, Button, Listbox, Scrollbar, Toplevel, PhotoImage, Canvas, messagebox

from sqlalchemy import create_engine, text

from configs.config_app_user import dbname, user, password, host, port

DATABASE_URL = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}'
engine = create_engine(DATABASE_URL)

ASSETS_PATH = Path(__file__).parent.parent / "build" / "assets" / "frame02"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class ProfileWindow(Frame):
    def __init__(self, parent, go_back_callback, switch_to_login):
        super().__init__(parent)
        self.configure(bg="#EEE2DC")

        self.go_back_callback = go_back_callback
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

        # Поле для поиска
        Label(self.content_frame, text="Поиск по названию игры:", bg="#EEE2DC", fg="#123C69", font=("Inter", 14)).grid(
            row=1, column=0, columnspan=2, pady=5, padx=10, sticky="w")
        self.search_entry = Entry(self.content_frame, width=50)
        self.search_entry.grid(row=2, column=0, columnspan=2, pady=5, padx=10, sticky="w")

        Button(self.content_frame, text="Найти", bg="#AC3B61", fg="white", command=self.search_reviews).grid(
            row=3, column=0, pady=5, padx=10, sticky="w")

        # Список отзывов
        self.listbox = Listbox(self.content_frame, width=80, height=15)
        self.listbox.grid(row=4, column=0, columnspan=1, pady=10, padx=20, sticky="w")

        # Скроллбар для списка
        scrollbar = Scrollbar(self.content_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=4, column=1, pady=10, padx=0, sticky="ns")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Кнопки управления
        Button(self.content_frame, text="Редактировать", bg="#AC3B61", fg="white", command=self.edit_review).grid(
            row=5, column=0, pady=10, padx=10, sticky="w")
        Button(self.content_frame, text="Удалить", bg="#AC3B61", fg="white", command=self.delete_review).grid(
            row=5, column=1, pady=10, padx=10, sticky="w")
        Button(self.content_frame, text="Назад", bg="#AC3B61", fg="white", command=self.go_back_callback).grid(
            row=6, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        self.load_reviews()

    def load_reviews(self):
        """Загружает отзывы пользователя из базы данных и отображает их"""
        user_id = self.master.current_user_id  # Получаем текущий UserID

        # Если пользователь не авторизован, ничего не делаем
        if not user_id:
            return

        try:
            with engine.connect() as connection:
                # Вызываем SQL-функцию и преобразуем результат в словари
                result = connection.execute(
                    text("SELECT * FROM users.get_reviews_by_user(:user_id)"),
                    {"user_id": user_id}
                ).mappings().all()  # Используем mappings() для доступа по ключам

            # Сохраняем загруженные отзывы
            self.loaded_reviews = [dict(row) for row in result]  # Преобразуем в список словарей

            # Обновляем Listbox
            self.reviews = {
                row["gametitle"]: f"{row['rating']}/10 - {row['comment']}" for row in self.loaded_reviews
            }
            self.update_listbox()

        except Exception as e:
            print(f"Ошибка загрузки отзывов: {e}")
            self.reviews = {}
            self.loaded_reviews = []

    def logout(self):
        self.master.current_user_id = None
        self.master.current_username = None
        self.switch_to_login()  # Возвращаемся на окно логина

    def refresh(self):
        """Обновляет отзывы для текущего пользователя"""
        self.load_reviews()
        self.username_label.config(text=f"Пользователь: {self.master.current_username}")

    def update_listbox(self):
        """Обновляет список отзывов в Listbox"""
        self.listbox.delete(0, 'end')
        for game, review in self.reviews.items():
            self.listbox.insert('end', f"{game}: {review}")

    def search_reviews(self):
        """Ищет отзывы по названию игры"""
        query = self.search_entry.get().lower()
        self.listbox.delete(0, 'end')
        for game, review in self.reviews.items():
            if query in game.lower():
                self.listbox.insert('end', f"{game}: {review}")

    def edit_review(self):
        """Редактирование выбранного отзыва"""
        selected = self.listbox.curselection()
        if not selected:
            return
        game = list(self.reviews.keys())[selected[0]]
        self.edit_review_popup(game)

    def delete_review(self):
        """Удаляет выбранный отзыв из базы данных"""
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите отзыв для удаления.")
            return

        # Получаем ReviewID выбранного отзыва
        review_title = self.listbox.get(selected[0]).split(":")[0]
        review_id = next((r["reviewid"] for r in self.loaded_reviews if r["gametitle"] == review_title), None)

        if not review_id:
            messagebox.showerror("Ошибка", "Не удалось определить ID отзыва.")
            return

        try:
            with engine.connect() as connection:
                connection.execute(
                    text("CALL users.delete_review(:review_id)"),
                    {"review_id": review_id}  # ID отзыва для удаления
                )
                connection.commit()

            # Удаляем отзыв из списка и обновляем Listbox
            self.reviews.pop(review_title, None)
            self.update_listbox()
            messagebox.showinfo("Успех", "Отзыв успешно удален.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить отзыв: {e}")

    def edit_review_popup(self, game_title):
        """Создает всплывающее окно для редактирования отзыва"""
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите отзыв для редактирования.")
            return

        # Находим ReviewID по названию игры
        review_id = next((r["reviewid"] for r in self.loaded_reviews if r["gametitle"] == game_title), None)

        if not review_id:
            messagebox.showerror("Ошибка", "Не удалось определить ID отзыва.")
            return

        # Открываем окно редактирования отзыва
        popup = Toplevel(self)
        popup.title("Редактировать отзыв")
        popup.geometry("500x400")
        popup.configure(bg="#EEE2DC")

        Label(popup, text=f"Редактировать отзыв для {game_title}", bg="#EEE2DC", fg="#123C69", font=("Inter", 14)).pack(
            pady=10)

        # Поле для редактирования текста отзыва
        current_comment = next((r["comment"] for r in self.loaded_reviews if r["gametitle"] == game_title), "")
        review_entry = Entry(popup, font=("Inter", 14), width=50)
        review_entry.insert(0, current_comment)
        review_entry.pack(pady=10, padx=20)

        # Выбор оценки через звездочки
        Label(popup, text="Ваша оценка:", font=("Inter", 16), bg="#EEE2DC", fg="#123C69").pack(pady=10, anchor="w")
        rating_frame = Frame(popup, bg="#EEE2DC")
        rating_frame.pack(pady=10)

        # Текущая оценка
        current_rating = next((r["rating"] for r in self.loaded_reviews if r["gametitle"] == game_title), 0)
        selected_rating = [current_rating]  # Храним выбранную оценку

        stars = []
        for i in range(1, 6):
            star_button = Button(
                rating_frame,
                text="★" if i <= current_rating // 2 else "☆",
                font=("Inter", 20),
                bg="#EEE2DC",
                fg="#AC3B61",
                command=lambda idx=i: set_rating(idx, stars)
            )
            star_button.grid(row=0, column=i - 1, padx=5)
            stars.append(star_button)

        def set_rating(idx, stars):
            """Обновляет выбранную оценку"""
            selected_rating[0] = idx * 2  # Преобразование в оценку от 1 до 10
            for star in stars:
                star.config(text="☆")  # Сбрасываем звездочки
            for j in range(idx):
                stars[j].config(text="★")  # Устанавливаем выбранные звездочки

        def save_review():
            """Сохраняет измененный отзыв"""
            new_comment = review_entry.get().strip()
            new_rating = selected_rating[0]

            if not new_comment or new_rating == 0:
                messagebox.showwarning("Предупреждение", "Заполните все поля и выберите оценку.")
                return

            try:
                with engine.connect() as connection:
                    # Обновляем комментарий
                    connection.execute(
                        text("CALL users.update_review(:review_id, :rating, :comment)"),
                        {
                            "review_id": review_id,  # ID отзыва
                            "rating": selected_rating[0],  # Новая оценка
                            "comment": new_comment  # Новый комментарий
                        }
                    )
                    connection.commit()

                # Обновляем данные в интерфейсе
                self.reviews[game_title] = f"{new_rating}/10 - {new_comment}"
                self.update_listbox()
                popup.destroy()
                messagebox.showinfo("Успех", "Отзыв успешно обновлен.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить отзыв: {e}")

        Button(popup, text="Сохранить", bg="#AC3B61", fg="white", font=("Inter", 14), command=save_review).pack(pady=20)

    def save_review(self, game, new_review, popup):
        """Сохраняет изменённый отзыв"""
        self.reviews[game] = new_review
        popup.destroy()
        self.update_listbox()

    def on_frame_configure(self, event):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
