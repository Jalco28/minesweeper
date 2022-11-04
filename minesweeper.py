import tkinter as tk

root = tk.Tk()
BOMB_IMAGE = tk.PhotoImage(file="bomb_icon.png")
FLAG_IMAGE = tk.PhotoImage(file="flag_icon.png")
BLANK_IMAGE = tk.PhotoImage(file="blank_tile.png")
TILE_SIZE = 30
info_frame = tk.Frame(height=30)
grid_frame = tk.Frame()

class Tile(tk.Button):
    def __init__(self, parent):
        super().__init__(parent, width=TILE_SIZE, height=TILE_SIZE)
        self.neighbours = None      #Stores number of adjacent bombs
        self.flagged = False        #If flagged by player
        self.bomb = None            #If tile is a bomb
        self.hidden = True          #If tile conented is hidden
        self.highlighted = False    #If highlighted by chording check
        self.config(image = BLANK_IMAGE)

    def __repr__(self) -> str:
         return "Tile"

tile_map = []

for i in range(14):         #Create tile_map
    temp = []
    for j in range(18):
        temp.append(Tile(grid_frame))
    tile_map.append(temp)

for row_idx, row in enumerate(tile_map):        #Grid tiles to gui
    for column_idx, tile in enumerate(row):
        tile.grid(row=row_idx, column=column_idx)


info_frame.pack()
grid_frame.pack()
root.mainloop()