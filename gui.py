import os

os.environ['TCL_LIBRARY'] = r'C:\Users\destep\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\destep\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

from tkinter import Tk
from gameback.main_window import MainWindow
from gameback.login_window import LoginWindow
from gameback.registration_window import RegistrationWindow


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Gameback")
        self.geometry("1094x668")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)

        # Хранилище для фреймов
        self.frames = {}

        # Изначально показываем окно входа
        self.show_frame(LoginWindow)

    def show_frame(self, frame_class):
        # Получаем уже созданный фрейм, если он есть
        frame = self.frames.get(frame_class)

        if not frame:
            # Если фрейм еще не создан, создаем его
            if frame_class == LoginWindow:
                frame = LoginWindow(self, lambda: self.show_frame(MainWindow),
                                    lambda: self.show_frame(RegistrationWindow))
            elif frame_class == MainWindow:
                frame = MainWindow(self,
                                   lambda: self.show_frame(LoginWindow))  # Передаем функцию для перехода на LoginWindow
            elif frame_class == RegistrationWindow:
                frame = RegistrationWindow(self, lambda: self.show_frame(LoginWindow))
            # Сохраняем фрейм в хранилище
            self.frames[frame_class] = frame

        # Скрываем все текущие виджеты
        for widget in self.winfo_children():
            widget.place_forget()

        # Отображаем новый фрейм
        frame.place(x=0, y=0, relwidth=1, relheight=1)  # Используем grid вместо pack


if __name__ == "__main__":
    app = App()
    app.mainloop()
