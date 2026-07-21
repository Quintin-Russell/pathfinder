import tkinter as tk # Gui
from collections import deque # BFS logic
import heapq # Dijkstra priority queue

# Grid dimestions
ROWS = 25
COLS = 25
CELL_SIZE = 24

# Animations
ANIMATION_DELAY = 20

# Cell states
EMPTY = 0
WALL = 1
START = 2
END = 3
WEIGHTED = 4

# Costs
WEIGHTED_COST = 5
NORMAL_COST = 1

# Colors
COLORS = {
    EMPTY: "white",
    WALL: "black",
    START: "green",
    END: "red",
    WEIGHTED: "#FFD580",
    "visited": "#87CEEB",
    "path": "yellow",
}

# holds state
class PathfinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinder Visualizer")

        self.grid_data = [[EMPTY for c in range(COLS)] for r in range(ROWS)]
        self.rect_ids = [[None for c in range(COLS)] for r in range(ROWS)]

        self.start = None
        self.end = None
        self.running = False

        self._build_controls()
        self._build_canvas()
        self._draw_grid()

    def _build_controls(self):
        direction_frame = tk.Frame(self.root)
        direction_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        direction_label = tk.Label(
            direction_frame,
            text="Draw walls by clicking or dragging. CTRL + click to set start and end. To add weighted squares, hover over the square and hit the W button",
            fg="gray"
        )
        direction_label.pack(side=tk.LEFT, padx=5)

        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.bfs_button = tk.Button(frame, text="BFS", command=self._run_bfs)
        self.dfs_button = tk.Button(frame, text="DFS", command=self._run_dfs)
        self.dijkstra_button = tk.Button(frame, text="Dijkstra", command=self._run_dijkstra)

        self.action_buttons = [self.bfs_button, self.dfs_button, self.dijkstra_button]

        for button in self.action_buttons:
            button.pack(side=tk.LEFT, padx=2)

        tk.Button(frame, text="Reset", command=self._reset_visited).pack(side=tk.LEFT, padx=2)
        tk.Button(frame, text="Clear All", command=self._clear_all).pack(side=tk.LEFT, padx=2)

        status_frame = tk.Frame(self.root)
        status_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.status_label = tk.Label(
            status_frame,
            text="",
            fg="blue"
        )
        self.status_label.pack(side=tk.RIGHT, padx=5)

    def _build_canvas(self):
        height = ROWS * CELL_SIZE
        width = COLS * CELL_SIZE
        self.canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            bg="white"
        )
        self.canvas.pack(padx=5, pady=5)

        self.canvas.bind("<Button-1>", self._on_left_click)
        self.canvas.bind("<B1-Motion>", self._on_left_drag)
        self.canvas.bind("<Control-Button-1>", self._on_ctrl_click)
        self.root.bind("w", self._on_weight_key)

    def _draw_grid(self):
        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y1 = r * CELL_SIZE
                y2 = y1 + CELL_SIZE

                rect_id = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="white",
                    outline="gray"
                )
                self.rect_ids[r][c] = rect_id

    # execute search algos
    def _run_bfs(self):
        if self._successful_pre_run_init("BFS"):
            queue = deque([self.start])
            visited = {self.start}
            came_from = {}
            visited_count = [0]

            def step():
                if not self.running:
                    return
                if not queue:
                    return self._stop_run("BFS", visited_count[0])

                current = queue.popleft()
                visited_count[0] += 1

                if current == self.end:
                    return self._output_found_path(came_from, visited_count[0])

                if current != self.start:
                    self._set_cell_fill(current[0], current[1], "visited")

                for neighbor in self._get_neighbors(current[0], current[1]):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        came_from[neighbor] = current
                        queue.append(neighbor)
                self.root.after(ANIMATION_DELAY, step)
            step()

    def _run_dfs(self):
        if self._successful_pre_run_init("DFS"):
            stack = [self.start]
            visited = {self.start}
            came_from = {}
            total_cost = {self.start: 0}
            visited_count = [0]

            def step():
                if not self.running:
                    return

                if not stack:
                    return self._stop_run("DFS", visited_count[0])

                current = stack.pop()
                visited_count[0] += 1

                if current == self.end:
                    return self._output_found_path(came_from, visited_count[0])

                if current != self.start:
                    self._set_cell_fill(current[0], current[1], "visited")

                for neighbor in self._get_neighbors(current[0], current[1]):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        came_from[neighbor] = current
                        stack.append(neighbor)

                self.root.after(ANIMATION_DELAY, step)

            step()

    def _run_dijkstra(self):
        if self._successful_pre_run_init("Dijkstra"):
            heap = [(0, self.start[0], self.start[1])]
            total_cost = {self.start: 0}

            came_from = {}
            visited = set()
            visited_count = [0]

            def step():
                if not self.running:
                    return
                if not heap:
                    return self._stop_run("Dijkstra", visited_count[0])

                cost, row, col = heapq.heappop(heap)
                current = (row, col)

                if current in visited:
                    self.root.after(1, step)
                    return
                visited.add(current)
                visited_count[0] += 1

                if current == self.end:
                    return self._output_found_path(came_from, visited_count[0])

                if current != self.start:
                    self._set_cell_fill(row, col, "visited")

                for nr, nc in self._get_neighbors(row, col):
                    neighbor = (nr, nc)
                    neighbor_state = self.grid_data[nr][nc]
                    move_cost = WEIGHTED_COST if neighbor_state == WEIGHTED else NORMAL_COST

                    new_cost = cost + move_cost
                    if neighbor not in total_cost or new_cost < total_cost[neighbor]:
                        total_cost[neighbor] = new_cost
                        came_from[neighbor] = current
                        heapq.heappush(heap, (new_cost, nr, nc))
                self.root.after(ANIMATION_DELAY, step)
            step()

    # reset methods
    def _reset_visited(self):
        self.running = False
        self._enable_all_buttons()
        for r in range(ROWS):
            for c in range(COLS):
                cell_state = self.grid_data[r][c]
                if cell_state in (EMPTY, WEIGHTED):
                    self._set_cell_fill(r, c, cell_state)

    def _clear_all(self):
        self.running = False
        self.start = None
        self.end = None
        self.status_label.config(text="")
        self._enable_all_buttons()
        for r in range(ROWS):
            for c in range(COLS):
                self._set_cell_info(r, c, EMPTY)

    # button methods
    def _disable_button(self, button):
        button.config(state="disabled")

    def _disable_all_buttons(self):
        for button in self.action_buttons:
            self._disable_button(button)

    def _enable_button(self, button):
        button.config(state="normal")

    def _enable_all_buttons(self):
        for button in self.action_buttons:
            self._enable_button(button)

    # click handlers
    def _on_left_click(self, event):
        if self.running:
            return
        row, col = self._get_cell(event)
        if row is None:
            return
        self._toggle_wall(row, col)

    def _on_left_drag(self, event):
        if self.running:
            return
        row, col = self._get_cell(event)
        if row is None:
            return
        if self.grid_data[row][col] == EMPTY:
            self._set_cell_info(row, col, WALL)

    def _on_ctrl_click(self, event):
        if self.running:
            return
        row, col = self._get_cell(event)
        if self.start is None:
            self.start = (row, col)
            self._set_cell_info(row, col, START)
        elif self.end is None:
            self.end = (row, col)
            self._set_cell_info(row, col, END)

    def _on_weight_key(self, _event):
        if self.running:
            return
        x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()

        col = x // CELL_SIZE
        row = y // CELL_SIZE

        if 0 <= row < ROWS and 0 <= col < COLS:
            cell_state = self.grid_data[row][col]
            if cell_state == EMPTY:
                self._set_cell_info(row, col, WEIGHTED)
            elif cell_state == WEIGHTED:
                self._set_cell_info(row, col, EMPTY)

    # helper methods
    def _get_cell(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            return row, col
        return None, None

    def _get_neighbors(self, row, col):
        neighbors = []
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and self.grid_data[nr][nc] != WALL:
                neighbors.append((nr, nc))
        return neighbors

    def _toggle_wall(self, row, col):
        cell_state = self.grid_data[row][col]
        if cell_state == EMPTY:
            self._set_cell_info(row, col, WALL)
        elif cell_state == WALL:
            self._set_cell_info(row, col, EMPTY)

    def _set_cell_info(self, row, col, value):
        self.grid_data[row][col] = value
        self._set_cell_fill(row, col, value)

    def _set_cell_fill(self, row, col, value):
        if value not in COLORS:
            return
        self.canvas.itemconfig(
            self.rect_ids[row][col],
            fill=COLORS[value]
        )

    def _trace_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        for r, c in path:
            if (r, c) != self.end:
                self._set_cell_fill(r, c, "path")
        return len(path)

    def _successful_pre_run_init(self, algorithm):
        should__stop_run = None in [self.start, self.end] or self.running
        if should__stop_run:
            self.status_label.config(
                text="Set start and end first (CTRL+click)",
                fg="red"
            )
            return False
        else:
            self._reset_visited()
            self.running = True
            self.status_label.config(
                text=f"Running {algorithm}...",
                fg="blue"
            )
            self._disable_all_buttons()
            return True

    def _stop_run(self, algorithm, visited_count):
        self.running = False
        self.status_label.config(
            text=f"{algorithm}: No path found. Visited: {visited_count}",
            fg="red"
        )
        self._enable_all_buttons()

    def _output_found_path(self, came_from, visited_count):
        path_len = self._trace_path(came_from, self.end)
        self.running = False
        self.status_label.config(
            text=f"We found a path! It takes {path_len} steps. We visited {visited_count} squares",
            fg="green"
        )
        self._enable_all_buttons()

def main():
    root = tk.Tk()
    app = PathfinderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
