from pathlib import Path
from tkinter import Canvas, Entry, Button, PhotoImage, Frame

ASSETS_PATH = Path(__file__).parent.parent / "build" / "assets" / "frame00"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class LoginWindow(Frame):
    def __init__(self, parent, switch_to_other, switch_to_main):
        super().__init__(parent)
        self.configure(bg="#FFFFFF")

        # Функция для переключения окон
        self.switch_to_other = switch_to_other
        self.switch_to_main = switch_to_main

        self.create_widgets()

    def create_widgets(self):
        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 741,
            width = 1180,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_rectangle(
            0.0,
            0.0,
            1180.0,
            741.0,
            fill="#EEE2DC",
            outline="")

        canvas.create_text(
            110.0,
            91.0,
            anchor="nw",
            text="Gameback",
            fill="#AC3B61",
            font=("Inter Bold", 72 * -1)
        )

        canvas.create_rectangle(
            102.0,
            259.0,
            489.0,
            577.0,
            fill="#EDC7B7",
            outline="")

        entry_1 = Entry(self, bd=2, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Arial", 12))
        entry_1.place(x=154.0, y=421.0, width=283.0, height=35.0)  # Позиционируем вручную

        canvas.create_rectangle(590.0, 0.0, 1180.0, 741.0, fill="#EDC7B7", outline="")

        entry_2 = Entry(self, bd=2, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Arial", 12))
        entry_2.place(x=154.0, y=331.0, width=283.0, height=35.0)

        canvas.create_text(146.0, 303.0, anchor="nw", text="ВОЙТИ, ИСПОЛЬЗУЯ ИМЯ АККАУНТА", fill="#123C69",
                           font=("Inter", 16 * -1))

        canvas.create_text(146.0, 396.0, anchor="nw", text="ПАРОЛЬ", fill="#123C69", font=("Inter", 16 * -1))
        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.switch_to_other,
            relief="flat"
        )
        button_1.image = button_image_1
        button_1.place(
            x=146.0,
            y=490.0,
            width=299.0,
            height=40.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        button_2 = Button(
            self,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.switch_to_main,
            relief="flat"
        )
        button_2.image = button_image_2
        button_2.place(
            x=228.0,
            y=538.0,
            width=129.0,
            height=26.0
        )

