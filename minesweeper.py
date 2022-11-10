import tkinter as tk
from functools import partial
import random

root = tk.Tk()
root.title('Minesweeper')
root.resizable(False, False)
ROWS = 14
COLUMNS = 18
BOMB_IMAGE = tk.PhotoImage(file="images/bomb_icon.png")
FLAG_IMAGE = tk.PhotoImage(file="images/flag_icon.png")
CLOCK_IMAGE = tk.PhotoImage(file="images/clock_icon.png")
debug = tk.PhotoImage("images/flag_icon.png")
NUMBER_IMAGES = {0: tk.PhotoImage(file="images/blank_tile.png", name='blank'),
                 1: tk.PhotoImage(file="images/1.png"),
                 2: tk.PhotoImage(file="images/2.png"),
                 3: tk.PhotoImage(file="images/3.png"),
                 4: tk.PhotoImage(file="images/4.png"),
                 5: tk.PhotoImage(file="images/5.png"),
                 6: tk.PhotoImage(file="images/6.png"),
                 7: tk.PhotoImage(file="images/7.png"),
                 8: tk.PhotoImage(file="images/8.png")}
TILE_SIZE = 30
root.wm_iconphoto(False, BOMB_IMAGE)
game_over = False
w_down = False
time = "0"
flags_to_place = 40
tiles_to_click = 212
info_frame = tk.Frame(height=30, name="frame_info")
grid_frame = tk.Frame(name="frame_grid")
bombs_generated = False


class Tile(tk.Button):
    def __init__(self, parent, row, column):
        super().__init__(parent, width=TILE_SIZE, height=TILE_SIZE,
                         image=NUMBER_IMAGES[0], bg='gray', activebackground='gray')
        self.neighbours = []  # Stores list of adjacent tile widgets
        self.flag_neighbours = 0
        self._flagged = False  # If flagged by player
        self.bomb = False  # If tile is a bomb
        self.hidden = True  # If tile contents is hidden
        self._highlighted = False  # If highlighted by chording check
        self.display_number = 0
        self.row = row
        self.column = column

        self.bind('<Button-3>', self.toggle_flagged)
        self.bind('<Enter>', partial(self.set_highlight, True))
        self.bind('<Leave>', partial(self.set_highlight, False))
        self.bind('<Button-1>', partial(self.click, True))

    def __repr__(self) -> str:
        return "Tile"

    def define_neighbours(self):
        relative_neighbour_coords = [[-1, -1], [-1, 0], [-1, 1],
                                     [0, -1],          [0, 1],
                                     [1, -1], [1, 0], [1, 1]]
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
        self.config(image=image)

    def set_highlight(self, value,  *args):
        if game_over:
            return
        if w_down:
            self.set_neighbours_highlight(value)
        else:
            self.set_neighbours_highlight(False)
        if self.hidden:
            self._highlighted = value
            if self._highlighted:
                self.config(bg='#D6d8d8', activebackground='#D6d8d8')
            else:
                self.config(bg='gray', activebackground='gray')

    def set_neighbours_highlight(self, value,  *args):
        if game_over:
            return
        for item in self.neighbours:
            if item.hidden:
                item._highlighted = value
                if item._highlighted:
                    item.config(bg='#D6d8d8', activebackground='#D6d8d8')
                else:
                    item.config(bg='gray', activebackground='gray')

    def toggle_flagged(self, *args):
        global flags_to_place
        if self.hidden and not game_over:
            self._flagged = False if self._flagged else True  # Togggle between True and False
            if self._flagged:
                self.set_image(FLAG_IMAGE)
                flags_to_place -= 1
                flags_left_label.config(text=flags_to_place)
            else:
                self.set_image(NUMBER_IMAGES[0])
                flags_to_place += 1
                flags_left_label.config(text=flags_to_place)
            for neighbour in self.neighbours:
                if self._flagged:
                    neighbour.flag_neighbours += 1
                else:
                    neighbour.flag_neighbours -= 1
                    pass

    def click(self, recurse, *args):
        global game_over, tiles_to_click
        if w_down and recurse and self.display_number == self.flag_neighbours:
            for neighbour in self.neighbours:
                neighbour.click(False)
        if self.hidden == False or game_over or self._flagged:
            return
        if not bombs_generated:
            generate_bombs(self.row, self.column)
            define_display_numbers()
        self.hidden = False
        tiles_to_click -= 1
        self.config(bg="#B3b3b3", activebackground="#B3b3b3")
        if self.bomb:
            run_game_over(False)
            self.config(bg='red')
        else:
            self.set_image(NUMBER_IMAGES[self.display_number])
            if tiles_to_click == 0:
                run_game_over(True)

        if self.display_number == 0:
            for neighbour in self.neighbours:
                neighbour.click(True if recurse else False)


def generate_bombs(preserve_row, preserve_column):
    global bombs_generated
    bombs_generated = True
    full_list = []
    bomb_list = []
    choices_left = 40
    for row in tile_map:
        for tile in row:
            if tile.row != preserve_row and tile.column != preserve_column:
                full_list.append(tile)
    while choices_left > 0:
        tile = random.choice(full_list)
        if tile not in bomb_list:
            bomb_list.append(tile)
            choices_left -= 1
    for tile in bomb_list:
        tile.bomb = True


def define_display_numbers():
    for row in tile_map:
        for tile in row:
            for neighbour in tile.neighbours:
                if neighbour.bomb:
                    tile.display_number += 1


def run_game_over(win):
    global game_over
    game_over = True
    if win:
        for row in tile_map:
            for tile in row:
                if tile.bomb:
                    if tile.cget('image') == 'blank':
                        tile.set_image(BOMB_IMAGE)
                        tile.hidden = False
                    tile.config(bg="#138808", activebackground="#138808")

    else:
        for row in tile_map:
            for tile in row:
                if tile.bomb:
                    tile.set_image(BOMB_IMAGE)
                    tile.hidden = False
                    tile.config(bg="#B3b3b3", activebackground="#B3b3b3")


def force_update_highlight(value):
    x, y = root.winfo_pointerxy()
    widget = root.winfo_containing(x, y)
    widget.set_neighbours_highlight(value)


def update_timer_label():
    global time
    if game_over:
        return
    time = str(int(time)+1)
    timer_label.config(text=time)
    root.after(1000, update_timer_label)


def key_pressed(event):
    global w_down
    if not w_down:
        if event.char.lower() == 'w':
            w_down = True
            force_update_highlight(True)


def key_released(event):
    global w_down
    if event.char.lower() == 'w':
        w_down = False
        force_update_highlight(False)


tile_map = []

for i in range(ROWS):  # Create tile_map
    temp = []
    for j in range(COLUMNS):
        temp.append(Tile(grid_frame, i, j))
    tile_map.append(temp)

for row_idx, row in enumerate(tile_map):  # Grid tiles to gui
    for column_idx, tile in enumerate(row):
        tile.grid(row=row_idx, column=column_idx)

for row in tile_map:
    for tile in row:
        tile.define_neighbours()


# Setup info pane
flag_image_label = tk.Label(info_frame, image=FLAG_IMAGE)
flag_image_label.pack(side='left')
flags_left_label = tk.Label(
    info_frame, text=flags_to_place, font="Helvetica 20")
flags_left_label.pack(side='left')

timer_image_label = tk.Label(info_frame, image=CLOCK_IMAGE)
timer_image_label.pack(side='left', padx=(30, 0))
timer_label = tk.Label(info_frame, text=time, font="Helvetica 20")
timer_label.pack(side='left')
update_timer_label()

root.bind("<KeyPress>", key_pressed)
root.bind("<KeyRelease>", key_released)

info_frame.pack()
grid_frame.pack()
root.mainloop()
