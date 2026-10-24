import turtle
import random

# Setup Layar Game
screen = turtle.Screen()
screen.title("Modern Tetris - Python Project")
screen.bgcolor("#1a1a2e")
screen.setup(width=500, height=700)
screen.tracer(0)

# Pen untuk menggambar grid/blok
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

# Pen khusus untuk teks UI (Skor & Game Over) supaya tidak berkedip
ui_pen = turtle.Turtle()
ui_pen.speed(0)
ui_pen.hideturtle()

# Konfigurasi Grid Tetris
BLOCK_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20
START_X = -125
START_Y = 225

# Bentuk Blok Tetriminos & Warnanya
SHAPES = [
    [[1, 1, 1, 1]],                 # I
    [[1, 1], [1, 1]],               # O
    [[0, 1, 0], [1, 1, 1]],         # T
    [[0, 1, 1], [1, 1, 0]],         # S
    [[1, 1, 0], [0, 1, 1]],         # Z
    [[1, 0, 0], [1, 1, 1]],         # J
    [[0, 0, 1], [1, 1, 1]]          # L
]
COLORS = ["#00f0f0", "#f0f000", "#a000f0", "#00f000", "#f00000", "#0000f0", "#f0a000"]

# Matriks Papan Permainan
grid = [["" for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

class Tetris:
    def __init__(self):
        self.score = 0
        self.game_over = False
        self.spawn_piece()
        
    def spawn_piece(self):
        self.shape_idx = random.randint(0, len(SHAPES)-1)
        self.shape = [row[:] for row in SHAPES[self.shape_idx]]
        self.color = COLORS[self.shape_idx]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        if self.check_collision(self.x, self.y, self.shape):
            self.game_over = True

    def check_collision(self, offset_x, offset_y, shape):
        for r_idx, row in enumerate(shape):
            for c_idx, val in enumerate(row):
                if val:
                    new_x = offset_x + c_idx
                    new_y = offset_y + r_idx
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return True
                    if new_y >= 0 and grid[new_y][new_x] != "":
                        return True
        return False

    def merge(self):
        for r_idx, row in enumerate(self.shape):
            for c_idx, val in enumerate(row):
                if val:
                    grid[self.y + r_idx][self.x + c_idx] = self.color
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        global grid
        new_grid = [row for row in grid if any(cell == "" for cell in row)]
        cleared = GRID_HEIGHT - len(new_grid)
        if cleared > 0:
            self.score += cleared * 100
            empty_rows = [["" for _ in range(GRID_WIDTH)] for _ in range(cleared)]
            grid = empty_rows + new_grid

    def move_left(self):
        if not self.game_over and not self.check_collision(self.x - 1, self.y, self.shape):
            self.x -= 1

    def move_right(self):
        if not self.game_over and not self.check_collision(self.x + 1, self.y, self.shape):
            self.x += 1

    def move_down(self):
        if not self.game_over:
            if not self.check_collision(self.x, self.y + 1, self.shape):
                self.y += 1
            else:
                self.merge()

    def rotate(self):
        if not self.game_over:
            rotated = [list(row) for row in zip(*self.shape[::-1])]
            if not self.check_collision(self.x, self.y, rotated):
                self.shape = rotated

game = Tetris()

def draw_square(x, y, color):
    pen.up()
    pen.goto(START_X + x * BLOCK_SIZE, START_Y - y * BLOCK_SIZE)
    pen.down()
    pen.fillcolor(color)
    pen.pencolor("#16213e")
    pen.begin_fill()
    for _ in range(4):
        pen.forward(BLOCK_SIZE - 1)
        pen.right(90)
    pen.end_fill()

def draw_board():
    pen.clear()
    
    # Bingkai Area Bermain
    pen.up()
    pen.goto(START_X - 5, START_Y + 5)
    pen.down()
    pen.pencolor("#e94560")
    pen.pensize(3)
    for _ in range(2):
        pen.forward(GRID_WIDTH * BLOCK_SIZE + 10)
        pen.right(90)
        pen.forward(GRID_HEIGHT * BLOCK_SIZE + 10)
        pen.right(90)
    pen.pensize(1)

    # Gambar Blok yang sudah menetap di grid
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            if grid[r][c] != "":
                draw_square(c, r, grid[r][c])

    # Gambar Blok yang sedang jatuh
    if not game.game_over:
        for r_idx, row in enumerate(game.shape):
            for c_idx, val in enumerate(row):
                if val:
                    draw_square(game.x + c_idx, game.y + r_idx, game.color)

    # Update Tampilan Skor UI secara terpisah agar stabil
    ui_pen.clear()
    ui_pen.up()
    ui_pen.goto(0, 260)
    ui_pen.pencolor("white")
    ui_pen.write(f"SCORE: {game.score}", align="center", font=("Courier", 18, "bold"))

    # Tampilan Game Over
    if game.game_over:
        ui_pen.goto(0, 0)
        ui_pen.pencolor("#ff4757")
        ui_pen.write("GAME OVER", align="center", font=("Courier", 26, "bold"))

    screen.update()

# Fungsi Kontrol dengan Auto-Render agar responsif saat tombol ditekan
def key_left():
    game.move_left()
    draw_board()

def key_right():
    game.move_right()
    draw_board()

def key_down():
    game.move_down()
    draw_board()

def key_rotate():
    game.rotate()
    draw_board()

# Hubungkan Keyboard
screen.listen()
screen.onkeypress(key_left, "Left")
screen.onkeypress(key_right, "Right")
screen.onkeypress(key_down, "Down")
screen.onkeypress(key_rotate, "Up")

# Game Loop Utama (Otomatis turun setiap 150 milidetik)
def update_game():
    if not game.game_over:
        game.move_down()
        draw_board()
        screen.ontimer(update_game, 150)
    else:
        draw_board()

draw_board()
screen.ontimer(update_game, 150)
turtle.done()