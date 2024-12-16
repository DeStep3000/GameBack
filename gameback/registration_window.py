from pathlib import Path
from tkinter import Frame, Canvas, Entry, Button, PhotoImage, messagebox
from sqlalchemy import create_engine, text
from configs.config_app_user import dbname, user, password, host, port

ASSETS_PATH = Path(__file__).parent.parent / "build" / "assets" / "frame01"

DATABASE_URL = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}'
engine = create_engine(DATABASE_URL)


def register_user(username, password, confirm_password, switch_to_login):
    if not username or not password or not confirm_password:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return

    if password != confirm_password:
        messagebox.showerror("Ошибка", "Пароли не совпадают!")
        return

    try:
        with engine.connect() as connection:
            connection.execute(
                text("CALL auth.add_user(:p_username, :p_password, :p_role)"),
                {"p_username": username, "p_password": password, "p_role": "user"},
            )
            connection.commit()
        switch_to_login()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Придумайте другой логин")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class RegistrationWindow(Frame):
    def __init__(self, parent, switch_to_login):
        super().__init__(parent)
        self.configure(bg="#FFFFFF")
        self.place(x=0, y=0, relwidth=1, relheight=1)

        self.switch_to_login = switch_to_login

        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=668,
            width=1094,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            0.0,
            0.0,
            1180.0,
            741.0,
            fill="#EEE2DC",
            outline="")

        canvas.create_text(
            171.0,
            135.0,
            anchor="nw",
            text="Регистрация",
            fill="#AC3B61",
            font=("InknutAntiqua Regular", 48 * -1)
        )

        canvas.create_text(
            138.0,
            66.0,
            anchor="nw",
            text="Gameback",
            fill="#AC3B61",
            font=("Inter Bold", 72 * -1)
        )

        canvas.create_rectangle(
            106.0,
            232.0,
            493.0,
            606.0,
            fill="#EDC7B7",
            outline="")

        canvas.create_text(
            145.0,
            442.0,
            anchor="nw",
            text="Повторите пароль",
            fill="#123C69",
            font=("Inter", 16 * -1)
        )

        self.username_entry = Entry(
            self,
            bd=2,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.username_entry.place(
            x=153.0,
            y=299.0,
            width=283.0,
            height=35.0
        )

        self.password_entry = Entry(
            self,
            bd=2,
            bg="#FFFFFF",
            fg="#000716",
            show="*",
            highlightthickness=0
        )
        self.password_entry.place(
            x=153.0,
            y=385.0,
            width=283.0,
            height=35.0
        )

        self.confirm_password_entry = Entry(
            self,
            bd=2,
            bg="#FFFFFF",
            fg="#000716",
            show="*",
            highlightthickness=0
        )
        self.confirm_password_entry.place(
            x=153.0,
            y=474.0,
            width=283.0,
            height=35.0
        )

        canvas.create_text(
            146.0,
            259.0,
            anchor="nw",
            text="Имя",
            fill="#123C69",
            font=("Inter", 16 * -1)
        )

        canvas.create_text(
            145.0,
            353.0,
            anchor="nw",
            text="Пароль",
            fill="#123C69",
            font=("Inter", 16 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        register_button = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_register,  # Вызываем обработчик
            relief="flat"
        )
        register_button.place(
            x=146.0,
            y=531.0,
            width=299.0,
            height=40.0
        )

        # Кнопка "Назад"
        back_button = Button(
            self, text="Назад",
            bg="#F44336", fg="white", font=("Inter", 14),
            borderwidth=0, highlightthickness=0,
            command=self.switch_to_login  # Возвращаемся на экран логина
        )
        back_button.place(x=146.0, y=590.0, width=299.0, height=40.0)

    def handle_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        register_user(username, password, confirm_password, self.switch_to_login)
