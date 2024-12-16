from pathlib import Path

from tkinter import Tk, Canvas, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Python\gui\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1094x668")
window.configure(bg="#EEE2DC")

canvas = Canvas(
    window,
    bg="#EEE2DC",
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
    1094.0,
    58.0,
    fill="#EDC7B7",
    outline="")

canvas.create_text(
    28.0,
    16.0,
    anchor="nw",
    text="Gameback",
    fill="#AC3B61",
    font=("InknutAntiqua Regular", 40 * -1)
)

canvas.create_rectangle(
    207.0,
    100.0,
    1034.0,
    284.0,
    fill="#BAB2B5",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=405.0,
    y=232.0,
    width=149.0,
    height=36.0
)

canvas.create_text(
    241.0,
    118.0,
    anchor="nw",
    text="Valorant",
    fill="#AC3B61",
    font=("Inter SemiBold", 24 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=241.0,
    y=232.0,
    width=137.0,
    height=36.0
)

canvas.create_rectangle(
    207.0,
    326.0,
    1034.0,
    668.0,
    fill="#BED8F3",
    outline="")

canvas.create_rectangle(
    257.0,
    575.0,
    985.0,
    703.0,
    fill="#446A94",
    outline="")

canvas.create_rectangle(
    257.0,
    405.0,
    985.0,
    533.0,
    fill="#436A93",
    outline="")

canvas.create_text(
    28.0,
    95.0,
    anchor="nw",
    text="Игры",
    fill="#123C69",
    font=("Inter", 32 * -1)
)

canvas.create_text(
    241.0,
    344.0,
    anchor="nw",
    text="Отзывы",
    fill="#123C69",
    font=("Inter SemiBold", 24 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=996.0,
    y=9.0,
    width=40.0,
    height=40.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=291.0,
    y=29.0,
    width=44.0,
    height=28.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=339.0,
    y=28.0,
    width=107.0,
    height=29.0
)
window.resizable(False, False)
window.mainloop()
