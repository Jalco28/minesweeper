import tkinter as tk
from functools import partial

root = tk.Tk()
ROWS = 14
COLUMNS = 18
BOMB_IMAGE = tk.PhotoImage(file="images/bomb_icon.png")
FLAG_IMAGE = tk.PhotoImage(file="images/flag_icon.png")
CLOCK_IMAGE = tk.PhotoImage(file="images/clock_icon.png")
BLANK_IMAGE = tk.PhotoImage(file="images/blank_tile.png")
TILE_SIZE = 30
time = "0"
flags_to_place = 40
info_frame = tk.Frame(height=30)
grid_frame = tk.Frame()

class Tile(tk.Button):
    def __init__(self, parent, row, column):
        super().__init__(parent, width=TILE_SIZE, height=TILE_SIZE, image = BLANK_IMAGE, bg = 'gray',activebackground='gray')
        self.neighbours = []      #Stores number of adjacent bombs
        self._flagged = False     #If flagged by player
        self.bomb = None          #If tile is a bomb
        self.hidden = True        #If tile conentents is hidden
        self._highlighted = False #If highlighted by chording check
        self.row = row
        self.column = column

        self.bind('<ButtonPress-2>', partial(self.set_neighbours_highlight, True))
        self.bind('<ButtonRelease-2>', partial(self.set_neighbours_highlight, False))
        self.bind('<Button-3>', self.toggle_flagged)
        self.bind('<Enter>', partial(self.set_highlight, True))
        self.bind('<Leave>', partial(self.set_highlight, False))
        self.bind('<Motion>')

    def __repr__(self) -> str:
         return "Tile"

    def set_neighbours(self):
        relative_neighbour_coords = [[-1,-1], [-1,0], [-1,1],
                                     [0,-1],          [0,1],
                                     [1,-1], [1,0], [1,1]]
        absolute_neighbour_coords = []
        for item in relative_neighbour_coords:
            new_row = self.row + item[0]
            new_column = self.column + item[1]
            if new_row < 0 or new_row > ROWS-1:
                continue
            if new_column < 0 or new_column > COLUMNS-1:
                continue
            absolute_neighbour_coords.append([new_row, new_column])
        for item in absolute_neighbour_coords:
            self.neighbours.append(tile_map[item[0]][item[1]])

    def set_image(self, image):
            self.config(image = image)

    def set_highlight(self, value,  *args):
        if self.hidden == True:
            self._highlighted = value
            if self._highlighted:
                self.config(bg='#b8b8b8', activebackground='#b8b8b8')
            else:
                self.config(bg = 'gray', activebackground='gray')

    def set_neighbours_highlight(self, value,  *args):
        for item in self.neighbours:
            if item.hidden == True:
                item._highlighted = value
                if item._highlighted:
                    item.config(bg='#b8b8b8', activebackground='#b8b8b8')
                else:
                    item.config(bg = 'gray', activebackground='gray')

    def toggle_flagged(self, *args):
        global flags_to_place
        self._flagged = False if self._flagged else True    #Togggle between True and False
        if self._flagged:
            self.set_image(FLAG_IMAGE)
            flags_to_place -= 1
            flags_left_label.config(text=flags_to_place)
        else:
            self.set_image(BLANK_IMAGE)
            flags_to_place += 1
            flags_left_label.config(text=flags_to_place)


def update_timer_label():
    global time
    time = str(int(time)+1)
    timer_label.config(text=time)
    root.after(1000, update_timer_label)

tile_map = []

for i in range(ROWS):         #Create tile_map
    temp = []
    for j in range(COLUMNS):
        temp.append(Tile(grid_frame, i, j))
    tile_map.append(temp)

for row_idx, row in enumerate(tile_map):        #Grid tiles to gui
    for column_idx, tile in enumerate(row):
        tile.grid(row=row_idx, column=column_idx)

for row in tile_map:
    for tile in row:
        tile.set_neighbours()


#Setup info pane
flag_image_label = tk.Label(info_frame, image = FLAG_IMAGE)
flag_image_label.pack(side='left')
flags_left_label = tk.Label(info_frame, text=flags_to_place, font="Helvetica 20")
flags_left_label.pack(side='left')

timer_image_label = tk.Label(info_frame, image=CLOCK_IMAGE)
timer_image_label.pack(side='left', padx=(30,0))
timer_label = tk.Label(info_frame, text = time, font="Helvetica 20")
timer_label.pack(side='left')
update_timer_label()

info_frame.pack()
grid_frame.pack()

root.mainloop()