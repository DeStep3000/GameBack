import os

os.environ['TCL_LIBRARY'] = r'C:\Users\destep\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\destep\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

from tkinter import Tk
from gameback.main_window import MainWindow
from gameback.login_window import LoginWindow
from gameback.registration_window import RegistrationWindow
from gameback.profile_window import ProfileWindow


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Gameback")
        self.geometry("1094x668")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)

        # Атрибуты для хранения текущего пользователя
        self.current_user_id = None
        self.current_username = None

        # Хранилище для фреймов
        self.frames = {}

        # Изначально показываем окно входа
        self.show_frame('LoginWindow')

    def show_main_window(self, user_id, username):
        self.current_user_id = user_id
        self.current_username = username
        frame = self.frames.get(MainWindow)
        if frame:
            frame.update_username()  # Обновляем имя пользователя
        self.show_frame('MainWindow')

    def show_frame(self, frame_name):
        # Преобразуем строку в класс, если нужно
        frame_class = {
            "MainWindow": MainWindow,
            "ProfileWindow": ProfileWindow,
            "LoginWindow": LoginWindow,
            "RegistrationWindow": RegistrationWindow
        }.get(frame_name, None)

        if not frame_class:
            raise ValueError(f"Неизвестное имя окна: {frame_name}")
        # Получаем уже созданный фрейм, если он есть
        frame = self.frames.get(frame_class)

        if not frame:
            if frame_class == LoginWindow:
                frame = LoginWindow(self, lambda user_id, username: self.show_main_window(user_id, username),
                                    lambda: self.show_frame('RegistrationWindow'))
            elif frame_class == MainWindow:
                frame = MainWindow(self, lambda: self.show_frame('LoginWindow'))

            elif frame_class == RegistrationWindow:
                frame = RegistrationWindow(self, lambda: self.show_frame('LoginWindow'))
            elif frame_class == ProfileWindow:
                frame = ProfileWindow(self, lambda: self.show_frame('MainWindow'))
            # Сохраняем фрейм в хранилище
            self.frames[frame_class] = frame
        else:
            # Обновляем фрейм при смене пользователя
            if hasattr(frame, "refresh"):
                frame.refresh()

        # Скрываем все текущие виджеты
        for widget in self.winfo_children():
            widget.place_forget()

        # Отображаем новый фрейм
        frame.place(x=0, y=0, relwidth=1, relheight=1)  # Используем grid вместо pack


if __name__ == "__main__":
    app = App()
    app.mainloop()
