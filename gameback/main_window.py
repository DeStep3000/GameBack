from tkinter import Tk, Canvas, Button, PhotoImage, Scrollbar, Frame, Toplevel, Label
from pathlib import Path

ASSETS_PATH = Path(__file__).parent.parent / "build" / "assets" / "frame02"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class MainWindow(Frame):
    def __init__(self, parent, switch_to_login):
        super().__init__(parent)
        self.configure(bg="#EEE2DC")

        self.switch_to_login = switch_to_login

        self.main_canvas = Canvas(self, bg="#EEE2DC", height=668,
                                  width=1094,
                                  bd=0,
                                  highlightthickness=0,
                                  relief="ridge")
        self.main_canvas.grid(row=0, column=0, sticky="nsew")

        self.main_scrollbar = Scrollbar(self, orient="vertical", command=self.main_canvas.yview)
        self.main_scrollbar.grid(row=0, column=1, sticky="ns")

        self.main_canvas.config(yscrollcommand=self.main_scrollbar.set)

        self.content_frame = Frame(self.main_canvas, bg="#EEE2DC")
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>", self.on_frame_configure)

        # Set row and column weights to make the layout responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Верхняя панель (header)
        self.header = Frame(self.content_frame, bg="#EDC7B7", height=58)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")  # Stretch header across the width
        Label(self.header, text="Gameback", bg="#EDC7B7", fg="#AC3B61", font=("InknutAntiqua Regular", 40)).pack(
            side="left", padx=20)

        # Статичные кнопки сверху
        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        Button(self.header, image=self.button_image_4, borderwidth=0, highlightthickness=0, command=lambda: print(
            "button_4 clicked"), relief="flat").pack(side="right", padx=5)

        self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        Button(self.header, image=self.button_image_5, borderwidth=0, highlightthickness=0, command=lambda: print(
            "button_5 clicked"), relief="flat").pack(side="right", padx=5)

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        Button(self.header, image=self.button_image_3, borderwidth=0, highlightthickness=0, command=self.switch_to_login, relief="flat").pack(side="right", padx=5)

        # Левая панель с кнопками (left_frame)
        self.left_frame = Frame(self.content_frame, bg="#EEE2DC", width=200)
        self.left_frame.grid(row=1, column=0, sticky="ns", padx=10, pady=10)

        # Правая панель с информацией и отзывами (right_frame)
        self.right_frame = Frame(self.content_frame, bg="#BAB2B5")
        self.right_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)  # Stretch the right panel

        # Название игры
        self.game_title = Label(self.right_frame, text="Игра 1", bg="#BAB2B5", fg="#123C69", font=("Inter", 18))
        self.game_title.pack(pady=10, padx=20, anchor="nw")

        # Описание игры
        self.game_description = Label(self.right_frame, text="Описание игры: Захватывающее приключение с элементами стратегии.", bg="#BAB2B5", fg="#123C69", font=("Inter", 14), wraplength=800, justify="left")
        self.game_description.pack(pady=5, padx=20, anchor="nw")

        # Кнопки "Подробнее" и "Оставить отзыв" перед отзывами
        self.button_details = Button(self.right_frame, text="Подробнее", bg="#AC3B61", fg="white",
                                     font=("Inter", 14), command=self.show_details)
        self.button_details.pack(pady=5, padx=20, anchor="w")

        self.button_review = Button(self.right_frame, text="Оставить отзыв", bg="#AC3B61", fg="white",
                                    font=("Inter", 14), command=self.leave_review)
        self.button_review.pack(pady=5, padx=20, anchor="w")

        # Список отзывов
        self.reviews_label = Label(self.right_frame, text="Отзывы:", bg="#BAB2B5", fg="#123C69", font=("Inter", 16))
        self.reviews_label.pack(pady=10, padx=20, anchor="nw")

        self.review1 = Label(self.right_frame, text="Отличная игра! Очень увлекательная.", bg="#BAB2B5", fg="#123C69", font=("Inter", 14), wraplength=800, justify="left")
        self.review1.pack(pady=5, padx=20, anchor="nw")

        self.review2 = Label(self.right_frame, text="Не хватает больше уровней, но все равно интересно.", bg="#BAB2B5", fg="#123C69", font=("Inter", 14), wraplength=800, justify="left")
        self.review2.pack(pady=5, padx=20, anchor="nw")

        # Генерация списка игр
        self.create_game_buttons()

    def create_game_buttons(self):
        # Пример списка игр с названием и описанием
        self.games = {
            "Игра 1": "Захватывающее приключение с элементами стратегии.",
            "Игра 2": "Динамичная игра с элементами экшн.",
            "Игра 3": "Интеллектуальная игра с головоломками.",
            "Игра 4": "Мифологическая игра с элементами RPG.",
            "Игра 5": "Классическая аркада с множеством уровней."
        }

        def on_game_button_click(game_name, description):
            self.update_game_info(game_name, description)

        for game_name, description in self.games.items():
            button = Button(self.left_frame, text=game_name, bg="#AC3B61", fg="white", font=("Inter", 14),
                            command=lambda g=game_name, desc=description: on_game_button_click(g, desc))
            button.pack(pady=5, padx=10, anchor="w")

    def update_game_info(self, game_name, description):
        # Обновляем название и описание игры
        self.game_title.config(text=game_name)
        self.game_description.config(text=f"Описание игры: {description}")

        # Обновляем отзывы (можно добавить сюда динамическое изменение)
        self.review1.config(text="Отличная игра! Очень увлекательная.")
        self.review2.config(text="Не хватает больше уровней, но все равно интересно.")

    def show_details(self):
        details_window = Toplevel(self)
        details_window.title("Подробнее")
        details_window.geometry("400x300")
        details_window.configure(bg="#EEE2DC")
        Label(details_window, text="Подробности об игре", font=("Inter", 16), bg="#EEE2DC", fg="#123C69").pack(
            pady=20)

    def leave_review(self):
        review_window = Toplevel(self)
        review_window.title("Оставить отзыв")
        review_window.geometry("400x300")
        review_window.configure(bg="#EEE2DC")
        Label(review_window, text="Оставьте ваш отзыв о игре", font=("Inter", 16), bg="#EEE2DC", fg="#123C69").pack(
            pady=20)

    def on_frame_configure(self, event):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))


if __name__ == "__main__":
    root = Tk()
    root.geometry("1500x700")
    root.title("Gameback")

    def switch_to_login():
        print("Switch to login page")

    app = MainWindow(root, switch_to_login)
    app.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()
