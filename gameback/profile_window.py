from tkinter import Frame, Label, Entry, Button, Listbox, Scrollbar, Toplevel

class ProfileWindow(Frame):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent)
        self.configure(bg="#EEE2DC")

        self.go_back_callback = go_back_callback

        # Заголовок
        Label(self, text="Мои отзывы", bg="#EEE2DC", fg="#123C69", font=("Inter", 20)).pack(pady=10)

        # Поле для поиска
        Label(self, text="Поиск по названию игры:", bg="#EEE2DC", fg="#123C69", font=("Inter", 14)).pack(pady=5)
        self.search_entry = Entry(self, width=50)
        self.search_entry.pack(pady=5)

        Button(self, text="Найти", bg="#AC3B61", fg="white", command=self.search_reviews).pack(pady=5)

        # Список отзывов
        self.listbox = Listbox(self, width=80, height=15)
        self.listbox.pack(pady=10, padx=20)

        # Скроллбар
        scrollbar = Scrollbar(self)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления
        Button(self, text="Редактировать", bg="#AC3B61", fg="white", command=self.edit_review).pack(side="left", padx=10)
        Button(self, text="Удалить", bg="#AC3B61", fg="white", command=self.delete_review).pack(side="left", padx=10)
        Button(self, text="Назад", bg="#AC3B61", fg="white", command=self.go_back_callback).pack(side="right", padx=10)

        # Заглушка данных отзывов
        self.reviews = {
            "Игра 1": "Хорошая игра, но можно было бы улучшить графику.",
            "Игра 2": "Понравилось, но уровни слишком короткие.",
        }
        self.update_listbox()

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
        """Удаление выбранного отзыва"""
        selected = self.listbox.curselection()
        if not selected:
            return
        game = list(self.reviews.keys())[selected[0]]
        del self.reviews[game]
        self.update_listbox()

    def edit_review_popup(self, game):
        """Создаёт всплывающее окно для редактирования отзыва"""
        popup = Toplevel(self)
        popup.title("Редактировать отзыв")
        popup.geometry("400x200")
        popup.configure(bg="#EEE2DC")

        Label(popup, text=f"Редактировать отзыв для {game}", bg="#EEE2DC", fg="#123C69", font=("Inter", 14)).pack(pady=10)
        review_entry = Entry(popup, width=50)
        review_entry.insert(0, self.reviews[game])
        review_entry.pack(pady=10)

        Button(popup, text="Сохранить", bg="#AC3B61", fg="white", command=lambda: self.save_review(game, review_entry.get(), popup)).pack(pady=10)

    def save_review(self, game, new_review, popup):
        """Сохраняет изменённый отзыв"""
        self.reviews[game] = new_review
        popup.destroy()
        self.update_listbox()
