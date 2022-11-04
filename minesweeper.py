import tkinter as tk

root = tk.Tk()
ROWS = 14
COLUMNS = 18
BOMB_IMAGE = tk.PhotoImage(file="bomb_icon.png")
FLAG_IMAGE = tk.PhotoImage(file="flag_icon.png")
BLANK_IMAGE = tk.PhotoImage(file="blank_tile.png")
TILE_SIZE = 30
flags_to_place = 40
info_frame = tk.Frame(height=30)
grid_frame = tk.Frame()

class Tile(tk.Button):
    def __init__(self, parent, row, column):
        super().__init__(parent, width=TILE_SIZE, height=TILE_SIZE, image = BLANK_IMAGE, bg = 'gray',activebackground='gray', command=self.toggle_flag)
        self.neighbours = []      #Stores number of adjacent bombs
        self._flagged = False        #If flagged by player
        self.bomb = None            #If tile is a bomb
        self.hidden = True          #If tile conentents is hidden
        self._highlighted = False    #If highlighted by chording check
        self.row = row
        self.column = column

    def __repr__(self) -> str:
         return "Tile"

    def set_neighbours(self):
        relative_neighbour_coords = [[-1,-1], [-1,0], [-1,1],
                                     [0,-1],          [0,1],
                                     [1,-1], [1,0], [1,1]]
        for item in relative_neighbour_coords:
            new_row = self.row + item[0]
            new_column = self.column + item[1]
            if new_row < 0 or new_row > ROWS:
                continue
            if new_column < 0 or new_column > COLUMNS:
                continue
            self.neighbours.append([new_row, new_column])

    def set_image(self, image):
            self.config(image = image)

    def toggle_highlight(self):
        self._highlighted = False if self._highlighted else True    #Togggle between True and False
        if self._highlighted:
            self.config(bg='#b8b8b8', activebackground='#b8b8b8')
        else:
            self.config(bg = 'gray', activebackground='gray')

    def toggle_flag(self):
        self._flagged = False if self._flagged else True    #Togggle between True and False
        if self._flagged:
            self.set_image(FLAG_IMAGE)
            flags_to_place -= 1
        else:
            self.set_image(BLANK_IMAGE)
            flags_to_place += 1


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

flag_image_label = tk.Label(info_frame, image = FLAG_IMAGE)
flag_image_label.pack(side='left')

info_frame.pack()
grid_frame.pack()
root.mainloop()