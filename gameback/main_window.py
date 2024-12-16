from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, Scrollbar, Frame, Toplevel

ASSETS_PATH = Path(__file__).parent.parent / "build" / "assets" / "frame02"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class MainWindow(Frame):
    def __init__(self, parent, switch_to_login):
        super().__init__(parent)
        self.configure(bg="#EEE2DC")

        self.switch_to_login = switch_to_login

        self.canvas = Canvas(
            self,
            bg="#EEE2DC",
            height=668,
            width=1094,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(x=1074, y=0, height=668)  # Размещаем вертикальную прокрутку

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        texts_from_db = [
            "Текст 1: Пример текста из базы данных",
            "Текст 2: Пример текста из базы данных",
            "Текст 3: Пример текста из базы данных",
            "Текст 4: Пример текста из базы данных",
            "Текст 5: Пример текста из базы данных",
            "Текст 6: Пример текста из базы данных",
            "Текст 7: Пример текста из базы данных",
            "Текст 8: Пример текста из базы данных",
            "Текст 9: Пример текста из базы данных",
            "Текст 10: Пример текста из базы данных"
        ]

        self.generate_text_blocks(texts_from_db)

        self.canvas.create_rectangle(
            0.0,
            0.0,
            1094.0,
            58.0,
            fill="#EDC7B7",
            outline="")

        self.canvas.create_text(
            28.0,
            16.0,
            anchor="nw",
            text="Gameback",
            fill="#AC3B61",
            font=("InknutAntiqua Regular", 40 * -1)
        )

        self.canvas.create_rectangle(
            198.0,
            83.0,
            1025.0,
            284.0,
            fill="#BAB2B5",
            outline="")

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.image = button_image_1
        button_1.place(
            x=405.0,
            y=232.0,
            width=149.0,
            height=36.0
        )

        self.canvas.create_text(
            241.0,
            128.0,
            anchor="nw",
            text="\n",
            fill="#AC3B61",
            font=("Inter SemiBold", 24 * -1)
        )

        self.canvas.create_text(
            241.0,
            91.0,
            anchor="nw",
            text="\n",
            fill="#AC3B61",
            font=("Inter SemiBold", 24 * -1)
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        button_2 = Button(
            self,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_details,
            relief="flat"
        )
        button_2.image = button_image_2
        button_2.place(
            x=241.0,
            y=232.0,
            width=137.0,
            height=36.0
        )

        self.canvas.create_text(
            28.0,
            77.0,
            anchor="nw",
            text="Игры",
            fill="#123C69",
            font=("Inter", 32 * -1)
        )

        self.canvas.create_text(
            238.0,
            300.0,
            anchor="nw",
            text="Отзывы",
            fill="#123C69",
            font=("Inter", 24, "bold")
        )

        button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        button_3 = Button(
            self,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.switch_to_login,
            relief="flat"
        )
        button_3.image = button_image_3
        button_3.place(
            x=996.0,
            y=9.0,
            width=40.0,
            height=40.0
        )

        button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        button_4 = Button(
            self,
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        button_4.image = button_image_4
        button_4.place(
            x=291.0,
            y=29.0,
            width=44.0,
            height=28.0
        )

        button_image_5 = PhotoImage(
            file=relative_to_assets("button_5.png"))
        button_5 = Button(
            self,
            image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        button_5.image = button_image_5
        button_5.place(
            x=332.0,
            y=28.0,
            width=113.0,
            height=29.0
        )

    def on_button_click(self):
        print("Button clicked, proceed to the next page")

    def show_details(self):
        # Создаем всплывающее окно
        details_window = Toplevel(self)
        details_window.title("Подробнее")
        details_window.geometry("400x300")
        details_window.configure(bg="#EEE2DC")

        details_window.grab_set()

        # Добавим в него текст или другие виджеты
        canvas = Canvas(details_window, bg="#EDC7B7", height=300, width=400, bd=0, highlightthickness=0,
                        relief="ridge")
        canvas.place(x=0, y=0)

        canvas.create_text(20, 20, anchor="nw", text="Об игре", fill="#AC3B61",
                           font=("Inter", 20, "bold"))

        details_window.mainloop()

    def generate_text_blocks(self, texts):
        """Генерируем прямоугольники и текстовые блоки на основе данных (например, из базы данных)."""
        y_position = 350
        # Начальная вертикальная позиция для текста
        for text in texts:
            # Добавляем прямоугольник для каждого текстового блока
            self.canvas.create_rectangle(200, y_position, 1010, y_position + 50, fill="#BAB2B5", outline="")
            self.canvas.create_text(200, y_position + 25, anchor="nw", text=text, fill="#123C69",
                                    font=("Inter SemiBold", 16))
            y_position += 60
