
import tkinter as tk
from tkinter import messagebox
from collections import deque
import random
import threading
import winsound

# ==========================================
# MAZE ESCAPE GAME - DAA PROJECT
# DFS + BFS + BACKTRACKING
# ==========================================

ROWS = 15
COLS = 21
CELL = 25

START = (1, 1)
GOAL = (ROWS - 2, COLS - 2)

# Colors
WALL = "#263445"
EMPTY = "#edf2f7"
PLAYER = "#ef4444"
START_COLOR = "#22c55e"
EXIT_COLOR = "#facc15"
PATH_COLOR = "#38bdf8"

# ==========================================
# BACKGROUND MUSIC USING WINSOUND
# ==========================================

sound_enabled = True
music_stop = threading.Event()

# Original simple electronic game melody
MELODY = [
    (523, 180), (659, 180), (784, 260),
    (659, 180), (784, 180), (880, 300),
    (784, 180), (659, 180), (587, 260),
    (523, 180), (587, 180), (659, 300)
]


def play_music():
    while not music_stop.is_set():
        for frequency, duration in MELODY:
            if music_stop.is_set():
                break
            try:
                winsound.Beep(frequency, duration)
            except RuntimeError:
                break


def start_music():
    music_stop.clear()
    threading.Thread(target=play_music, daemon=True).start()


def stop_music():
    music_stop.set()


def play_effect(frequency=900, duration=100):
    if sound_enabled:
        threading.Thread(
            target=lambda: winsound.Beep(frequency, duration),
            daemon=True
        ).start()


def toggle_sound():
    global sound_enabled

    sound_enabled = not sound_enabled

    if sound_enabled:
        sound_button.config(text="🔊 Sound: ON")
        start_music()
        play_effect(700, 120)
    else:
        sound_button.config(text="🔇 Sound: OFF")
        stop_music()


# ==========================================
# MAZE GENERATION USING BACKTRACKING
# ==========================================

def generate_maze():
    grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]

    grid[1][1] = 0

    def carve(r, c):
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            if (1 <= nr < ROWS - 1 and
                    1 <= nc < COLS - 1 and
                    grid[nr][nc] == 1):

                grid[r + dr // 2][c + dc // 2] = 0
                grid[nr][nc] = 0

                carve(nr, nc)

    carve(1, 1)

    # Open additional walls to create alternative routes
    for r in range(1, ROWS - 1):
        for c in range(1, COLS - 1):
            if grid[r][c] == 1 and random.random() < 0.15:
                grid[r][c] = 0

    grid[GOAL[0]][GOAL[1]] = 0

    return grid


maze = generate_maze()
player = list(START)
game_finished = False
current_path = []


# ==========================================
# FIND NEIGHBOURS
# ==========================================

def neighbours(position):
    r, c = position

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr = r + dr
        nc = c + dc

        if (0 <= nr < ROWS and
                0 <= nc < COLS and
                maze[nr][nc] == 0):
            yield (nr, nc)


# ==========================================
# DFS ALGORITHM
# ==========================================

def dfs():
    stack = [(START, [START])]
    visited = set()

    while stack:
        current, path = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        if current == GOAL:
            return path, len(visited)

        for nxt in neighbours(current):
            if nxt not in visited:
                stack.append((nxt, path + [nxt]))

    return [], len(visited)


# ==========================================
# BFS ALGORITHM
# ==========================================

def bfs():
    queue = deque([(START, [START])])
    visited = {START}

    while queue:
        current, path = queue.popleft()

        if current == GOAL:
            return path, len(visited)

        for nxt in neighbours(current):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))

    return [], len(visited)


# ==========================================
# BACKTRACKING ALGORITHM
# ==========================================

def backtracking():
    visited = set()
    path = []

    def solve(current):
        visited.add(current)
        path.append(current)

        if current == GOAL:
            return True

        for nxt in neighbours(current):
            if nxt not in visited:
                if solve(nxt):
                    return True

        path.pop()
        return False

    if solve(START):
        return path[:], len(visited)

    return [], len(visited)


# ==========================================
# GUI WINDOW
# ==========================================

root = tk.Tk()
root.title("MAZE ESCAPE - DAA PROJECT")
root.configure(bg="#101827")
root.geometry("950x650")
root.resizable(False, False)


# Heading
heading = tk.Label(
    root,
    text="MAZE ESCAPE",
    font=("Arial", 23, "bold"),
    fg="#38bdf8",
    bg="#101827"
)
heading.pack(pady=(8, 2))

subtitle = tk.Label(
    root,
    text="A DAA Game | DFS  •  BFS  •  Backtracking",
    font=("Arial", 10),
    fg="white",
    bg="#101827"
)
subtitle.pack(pady=(0, 8))


# Main frame
main_frame = tk.Frame(root, bg="#101827")
main_frame.pack(padx=12, pady=5)


# ==========================================
# MAZE CANVAS
# ==========================================

canvas = tk.Canvas(
    main_frame,
    width=COLS * CELL,
    height=ROWS * CELL,
    bg="#101827",
    highlightthickness=2,
    highlightbackground="#38bdf8"
)
canvas.grid(row=0, column=0, padx=(0, 15), sticky="n")


def draw_maze(path=None):
    canvas.delete("all")

    path = set(path or [])

    for r in range(ROWS):
        for c in range(COLS):

            x1 = c * CELL
            y1 = r * CELL
            x2 = x1 + CELL
            y2 = y1 + CELL

            pos = (r, c)

            if maze[r][c] == 1:
                color = WALL
            elif pos in path:
                color = PATH_COLOR
            else:
                color = EMPTY

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="#cbd5e1",
                width=1
            )

    # Start
    r, c = START
    canvas.create_rectangle(
        c * CELL + 2, r * CELL + 2,
        (c + 1) * CELL - 2, (r + 1) * CELL - 2,
        fill=START_COLOR, outline=""
    )
    canvas.create_text(
        c * CELL + CELL // 2,
        r * CELL + CELL // 2,
        text="S", font=("Arial", 12, "bold")
    )

    # Exit
    r, c = GOAL
    canvas.create_rectangle(
        c * CELL + 2, r * CELL + 2,
        (c + 1) * CELL - 2, (r + 1) * CELL - 2,
        fill=EXIT_COLOR, outline=""
    )
    canvas.create_text(
        c * CELL + CELL // 2,
        r * CELL + CELL // 2,
        text="E", font=("Arial", 12, "bold")
    )

    # Player
    r, c = player
    canvas.create_oval(
        c * CELL + 5, r * CELL + 5,
        (c + 1) * CELL - 5, (r + 1) * CELL - 5,
        fill=PLAYER,
        outline="white",
        width=2
    )


# ==========================================
# STATUS AND COMPARISON
# ==========================================

status = tk.Label(
    root,
    text="Use arrow keys or WASD to reach the exit!",
    font=("Arial", 10, "bold"),
    fg="#facc15",
    bg="#101827"
)
status.pack(pady=3)

result = tk.Label(
    root,
    text="Choose an algorithm to solve the maze.",
    font=("Consolas", 10, "bold"),
    fg="#38bdf8",
    bg="#101827",
    justify="left",
    anchor="w",
    width=75,
    height=14
)
result.pack(pady=8)


# ==========================================
# ALGORITHM BUTTON FUNCTIONS
# ==========================================

def solve_algorithm(name):
    global game_finished, current_path

    if name == "DFS":
        path, visited = dfs()

    elif name == "BFS":
        path, visited = bfs()

    else:
        path, visited = backtracking()

    if path:
        current_path = path
        draw_maze(path)
        game_finished = True

        status.config(text=f"{name} successfully found the exit!")
        result.config(
            text=f"{name} RESULTS\n"
                 f"Path length: {len(path) - 1} steps\n"
                 f"Cells visited: {visited}"
        )

        play_effect(950, 180)

    else:
        status.config(text="No path found!")



def compare_all():
    global game_finished, current_path

    # Run all three algorithms
    dfs_path, dfs_visited = dfs()
    bfs_path, bfs_visited = bfs()
    bt_path, bt_visited = backtracking()

    # Calculate results
    dfs_steps = len(dfs_path) - 1
    bfs_steps = len(bfs_path) - 1
    bt_steps = len(bt_path) - 1

    # Display comparison
    comparison = (
        "===== ALGORITHM COMPARISON =====\n\n"
        f"DFS:\n"
        f"Path Length: {dfs_steps} steps\n"
        f"Visited Cells: {dfs_visited}\n\n"

        f"BFS:\n"
        f"Path Length: {bfs_steps} steps\n"
        f"Visited Cells: {bfs_visited}\n\n"

        f"BACKTRACKING:\n"
        f"Path Length: {bt_steps} steps\n"
        f"Visited Cells: {bt_visited}\n\n"

        "BFS guarantees the shortest path!"
    )

    result.config(text=comparison)

    # Display BFS shortest path
    current_path = bfs_path
    draw_maze(current_path)

    game_finished = True

    status.config(
        text="All algorithms compared successfully!"
    )

    play_effect(1000, 200)


# ==========================================
# PLAYER MOVEMENT
# ==========================================

def move_player(event):
    global game_finished

    if game_finished:
        return

    key = event.keysym.lower()

    movements = {
        "up": (-1, 0),
        "w": (-1, 0),
        "down": (1, 0),
        "s": (1, 0),
        "left": (0, -1),
        "a": (0, -1),
        "right": (0, 1),
        "d": (0, 1)
    }

    if key not in movements:
        return

    dr, dc = movements[key]

    nr = player[0] + dr
    nc = player[1] + dc

    if maze[nr][nc] == 0:
        player[:] = [nr, nc]
        draw_maze(current_path)
        play_effect(600, 35)

        if tuple(player) == GOAL:
            game_finished = True
            status.config(text="YOU ESCAPED THE MAZE!")
            play_effect(1100, 350)
            messagebox.showinfo(
                "Congratulations!",
                "You successfully escaped the maze!"
            )


root.bind("<KeyPress>", move_player)


# ==========================================
# NEW MAZE BUTTON
# ==========================================

def new_maze():
    global maze, player, game_finished, current_path

    maze = generate_maze()
    player = list(START)
    game_finished = False
    current_path = []

    status.config(text="New maze generated! Find the exit.")
    result.config(text="Choose an algorithm to solve the maze.")

    draw_maze()
    play_effect(750, 120)


# ==========================================
# CONTROL PANEL
# ==========================================

panel = tk.Frame(main_frame, bg="#1e293b", padx=12, pady=12)
panel.grid(row=0, column=1, sticky="n")

tk.Label(
    panel,
    text="GAME CONTROLS",
    font=("Arial", 12, "bold"),
    fg="#38bdf8",
    bg="#1e293b"
).pack(pady=7)


def make_button(text, command, color):
    return tk.Button(
        panel,
        text=text,
        command=command,
        font=("Arial", 10, "bold"),
        bg=color,
        fg="white",
        activebackground="#475569",
        activeforeground="white",
        width=19,
        pady=5,
        relief="flat",
        cursor="hand2"
    )


make_button(
    "DFS SOLVE",
    lambda: solve_algorithm("DFS"),
    "#2563eb"
).pack(pady=4)

make_button(
    "BFS SOLVE",
    lambda: solve_algorithm("BFS"),
    "#0891b2"
).pack(pady=4)

make_button(
    "BACKTRACKING",
    lambda: solve_algorithm("BACKTRACKING"),
    "#7c3aed"
).pack(pady=4)

make_button(
    "COMPARE ALL",
    compare_all,
    "#15803d"
).pack(pady=4)

make_button(
    "GENERATE NEW MAZE",
    new_maze,
    "#ea580c"
).pack(pady=4)

sound_button = make_button(
    "🔊 Sound: ON",
    toggle_sound,
    "#475569"
)
sound_button.pack(pady=4)

make_button(
    "EXIT GAME",
    root.destroy,
    "#b91c1c"
).pack(pady=4)


# Instructions
tk.Label(
    panel,
    text="MOVE:\nArrow Keys / WASD\n\n"
         "GREEN = START\n"
         "YELLOW = EXIT\n"
         "RED = PLAYER\n"
         "BLUE = SOLUTION",
    font=("Arial", 9),
    fg="white",
    bg="#1e293b",
    justify="left"
).pack(pady=10)


# ==========================================
# START GAME
# ==========================================

draw_maze()
start_music()

root.protocol("WM_DELETE_WINDOW", lambda: (stop_music(), root.destroy()))

root.mainloop()
