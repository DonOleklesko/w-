import tkinter as tk
import random

WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

BG_COLOR = "#1e1e1e"
SNAKE_COLOR = "#00ff88"
FOOD_COLOR = "#ff5555"
TEXT_COLOR = "#ffffff"
BUTTON_COLOR = "#444444"
BUTTON_HOVER = "#666666"

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pyton w pythonie")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.create_buttons()
        self.reset_game()

        self.root.bind("<Key>", self.key_press)

    def create_buttons(self):
        self.btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.btn_frame.pack(pady=10)

        self.start_btn = tk.Button(self.btn_frame, text="▶️", command=self.start_game, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.pause_btn = tk.Button(self.btn_frame, text="⏸️", command=self.toggle_pause, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.reset_btn = tk.Button(self.btn_frame, text="🔁", command=self.reset_game, bg=BUTTON_COLOR, fg=TEXT_COLOR)

        for btn in [self.start_btn, self.pause_btn, self.reset_btn]:
            btn.config(font=("Arial", 12), width=10, relief="flat", activebackground=BUTTON_HOVER)
            btn.pack(side="left", padx=10)

    def reset_game(self):
        self.score = 0
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.food = self.spawn_food()
        self.direction = "Right"
        self.running = False
        self.paused = False
        self.draw()
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Kliknij START", fill=TEXT_COLOR, font=("Arial", 24, "bold"), tag="start_text")

    def spawn_food(self):
        while True:
            pos = (
                random.randint(0, (WIDTH // CELL_SIZE) - 1),
                random.randint(0, (HEIGHT // CELL_SIZE) - 1)
            )
            if pos not in self.snake:
                return pos

    def key_press(self, event):
        if event.keysym == "space":
            self.toggle_pause()
        elif event.keysym in DIRECTIONS:
            new_dir = event.keysym
            opposite = {
                "Up": "Down", "Down": "Up",
                "Left": "Right", "Right": "Left"
            }
            if new_dir != opposite.get(self.direction):
                self.direction = new_dir

    def start_game(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.canvas.delete("start_text")
            self.update()

    def toggle_pause(self):
        if self.running:
            self.paused = not self.paused
            self.pause_btn.config(text="▶️" if self.paused else "⏸️")

    def move(self):
        if self.paused:
            return

        dx, dy = DIRECTIONS[self.direction]
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

        if (
            new_head in self.snake or
            new_head[0] < 0 or new_head[1] < 0 or
            new_head[0] >= WIDTH // CELL_SIZE or
            new_head[1] >= HEIGHT // CELL_SIZE
        ):
            self.running = False
            self.draw()
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="GAME OVER ", fill="white", font=("Arial", 30, "bold"))
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.canvas.delete("all")

        for x, y in self.snake:
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=SNAKE_COLOR, outline=BG_COLOR
            )

        fx, fy = self.food
        self.canvas.create_oval(
            fx * CELL_SIZE, fy * CELL_SIZE,
            (fx + 1) * CELL_SIZE, (fy + 1) * CELL_SIZE,
            fill=FOOD_COLOR, outline=BG_COLOR
        )

        self.canvas.create_text(60, 15, text=f"Punkty: {self.score}", fill="white", font=("Arial", 14))

    def update(self):
        if self.running and not self.paused:
            self.move()
            self.draw()
        if self.running:
            self.root.after(100, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg=BG_COLOR)
    game = SnakeGame(root)
    root.mainloop()
