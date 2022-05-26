from Tiles import *
from Areas import *
from tkinter import *
from settings import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

class WindowApp:
    
    def __init__(self) -> None:
        self.initUI()
        self.root.mainloop()

    def initUI(self):
        root = Tk()
        root.configure(bg='grey')
        root.geometry(f"{WIDTH}x{HEIGHT}")

        left_frame = Frame(
            root,
            bg='white',
            height=HEIGHT,
            width=WIDTH//3
        )

        left_frame.place(x=0, y=0)

        main_frame = Frame(
            root,
            bg='grey',
            height=HEIGHT,
            width=WIDTH-WIDTH//3
        )

        main_frame.place(x=WIDTH//3, y=0)

        Tile.generate_map()
        Area.generate_areas()
        img = Image.fromarray(np.uint8(Tile.generate_color_map())).convert('RGB')
        # plt.imshow(img)
        # plt.show()
        self.tk_img = ImageTk.PhotoImage(img)
        canvas = Canvas(
            main_frame,
            bg='red',
            width=GRID_SIZE*TILE_SIZE,
            height=GRID_SIZE*TILE_SIZE,
            highlightthickness=0
        )
        canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        canvas.create_image(0, 0, anchor='nw', image=self.tk_img)
        canvas.bind("<Button-1>", self.left_click_canvas)
        canvas.bind("<Motion>", self.on_hover)

        lbl = Label(
            left_frame,
            bg='white',
            fg='black',
            text='Tile info...',
            font=("Lato", 18),
            justify='left'
        )
        lbl.place(x=0, y=0)
        self.root = root
        self.left_frame = left_frame
        self.main_frame = main_frame
        self.canvas = canvas
        self.canvas.create_image(0,0, anchor='nw', image=self.tk_img)
        self.lbl = lbl

    def show_map(self):
        plt.imshow(Tile.generate_color_map())
        plt.show()

    def left_click_canvas(self, event):
        y, x = event.x//TILE_SIZE, event.y//TILE_SIZE
        print(f"x={x}, y={y}")
        self.update_tile_label(f"x={x}, y={y}")
        print(Tile.all[x][y].get_tile_description())

    def on_hover(self, event):
        y, x = event.x//TILE_SIZE, event.y//TILE_SIZE
        txt = Tile.all[x][y].get_tile_description()
        self.update_tile_label(txt)
        
    def update_tile_label(self, txt):
        self.lbl.configure(text=txt)


# def left_click_canvas(event):
#     print(event)
#     print(f"x={event.x//TILE_SIZE}, y={event.y//TILE_SIZE}")

# root = Tk()
# root.configure(bg='grey')
# root.geometry(f"{WIDTH}x{HEIGHT}")

# left_frame = Frame(
#     root,
#     bg='white',
#     height=HEIGHT,
#     width=WIDTH//4
# )

# left_frame.place(x=0, y=0)

# main_frame = Frame(
#     root,
#     bg='grey',
#     height=HEIGHT,
#     width=WIDTH-WIDTH//4
# )

# main_frame.place(x=WIDTH//4, y=0)

# Tile.generate_map()
# Area.generate_areas()
# img = Image.fromarray(np.uint8(Tile.generate_color_map())).convert('RGB')
# tk_img = ImageTk.PhotoImage(img)
# canvas = Canvas(
#     main_frame,
#     bg='red',
#     width=GRID_SIZE*TILE_SIZE,
#     height=GRID_SIZE*TILE_SIZE,
#     highlightthickness=0
# )
# #canvas.pack(anchor='center')
# canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
# canvas.create_image(0, 0, anchor='nw', image=tk_img)
# canvas.bind("<Button-1>", left_click_canvas)
# print(canvas.winfo_width(), canvas.winfo_height())
# root.mainloop()

#show_map()
myapp = WindowApp()