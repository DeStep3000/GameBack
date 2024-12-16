from tkinter import Frame, Label, Button, PhotoImage


def create_header(parent, username, logout_callback, assets_path, show_main_window, show_profile_window):
    """Создает общий хедер для окон."""
    header = Frame(parent, bg="#EDC7B7", height=58)
    header.pack(fill="x")

    # Логотип
    Label(header, text="Gameback", bg="#EDC7B7", fg="#AC3B61", font=("InknutAntiqua Regular", 40)).pack(
        side="left", padx=20)

    # Имя пользователя
    Label(
        header, text=f"Пользователь: {username}",
        bg="#EDC7B7", fg="#123C69", font=("Inter", 14)
    ).pack(side="left", padx=10)

    # Кнопка "Выход"
    Button(
        header, text="Выход", bg="#AC3B61", fg="white",
        font=("Inter", 14), command=logout_callback
    ).pack(side="right", padx=10)

    # Кнопка "Игры"
    button_image_4 = PhotoImage(file=assets_path / "button_4.png")
    Button(
        header, image=button_image_4, borderwidth=0, highlightthickness=0,
        command=show_main_window, relief="flat"
    ).pack(side="right", padx=5)

    # Кнопка "Мои отзывы"
    button_image_5 = PhotoImage(file=assets_path / "button_5.png")
    Button(
        header, image=button_image_5, borderwidth=0, highlightthickness=0,
        command=show_profile_window, relief="flat"
    ).pack(side="right", padx=5)

    # Чтобы кнопки не пропали из-за сборки мусора
    header.button_image_4 = button_image_4
    header.button_image_5 = button_image_5

    return header
