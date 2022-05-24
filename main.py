from tiles import *
from areas import *
from tkinter import *
from settings import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

def show_map():
    plt.imshow(Tile.generate_color_map())
    plt.show()

def left_click_canvas(event):
    print(event)

root = Tk()
root.configure(bg='grey')
root.geometry(f"{WIDTH}x{HEIGHT}")

left_frame = Frame(
    root,
    bg='white',
    height=HEIGHT,
    width=WIDTH//4
)

left_frame.place(x=0, y=0)

main_frame = Frame(
    root,
    bg='grey',
    height=HEIGHT,
    width=WIDTH-WIDTH//4
)

main_frame.place(x=WIDTH//4, y=0)

Tile.generate_map()
Area.generate_areas()
img = Image.fromarray(np.uint8(Tile.generate_color_map())).convert('RGB').resize((500,500))
tk_img = ImageTk.PhotoImage(img)
canvas = Canvas(
    main_frame,
    width=500,
    height=500
)
#canvas.pack(anchor='center')
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
canvas.create_image(0, 0, anchor='nw', image=tk_img)
canvas.bind("<Button-1>", left_click_canvas)

root.mainloop()

#show_map()