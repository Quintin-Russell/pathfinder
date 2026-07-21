# 🧭 Pathfinding Algorithm Visualizer

An interactive Python desktop application that brings pathfinding algorithms to life. Draw mazes, add weighted cells, choose a starting and ending point, and watch **BFS, DFS, and Dijkstra's** explore the grid in real time.

This project demonstrates how different algorithms and underlying data structures—**queues, stacks, and priority queues**—produce dramatically different exploration patterns and pathfinding results.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![Algorithms](https://img.shields.io/badge/Algorithms-BFS%20%7C%20DFS%20%7C%20Dijkstra%20%7C%20A*-orange)
![Status](https://img.shields.io/badge/Status-Complete-success)

---

## 📌 Project Overview

Every time a maps application calculates directions, a pathfinding algorithm searches through many possible routes to find an appropriate path.

This project makes that process visible.

The application provides a **25 × 25 interactive grid** where users can:

* Draw and remove walls using the mouse
* Place a start point and end point
* Create weighted cells
* Run different pathfinding algorithms
* Watch cells being explored in real time
* Visualize the final path
* Compare algorithm performance and exploration patterns

The main goal is to understand how the choice of algorithm and data structure affects the way a graph is explored.

---

## ✨ Features

* 🖱️ Interactive maze creation with mouse controls
* 🟩 Custom start point placement
* 🟥 Custom end point placement
* ⬛ Wall drawing with click-and-drag
* 🟧 Weighted cells with configurable traversal costs
* 🔵 Real-time exploration animation
* 🟨 Final path visualization
* 🔄 Reset visited cells without removing the maze
* 🗑️ Clear the entire grid
* 📊 Visited-cell statistics
* 💰 Path cost reporting for weighted algorithms

---

## 🧠 Algorithms Implemented

### 1. Breadth-First Search (BFS)

BFS explores the grid **level by level**, spreading outward from the starting point.

It uses a **FIFO (First In, First Out) queue** implemented with Python's `deque`.

```text
Start
  ↓
Explore all cells 1 step away
  ↓
Explore all cells 2 steps away
  ↓
Explore all cells 3 steps away
  ↓
...
```

Because BFS explores an unweighted grid in layers, the first path it finds to the destination is guaranteed to have the **fewest number of steps**.

**Data structure:** Queue
**Python implementation:** `collections.deque`
**Optimal for:** Unweighted shortest-path problems
**Considers weights:** No

---

### 2. Depth-First Search (DFS)

DFS takes a different approach. Instead of spreading outward evenly, it dives as deeply as possible along one path before backtracking.

DFS uses a **LIFO (Last In, First Out) stack**.

In this project, a standard Python list is used as the stack:

```python
stack.append(neighbor)
stack.pop()
```

The switch from a queue to a stack creates a dramatically different exploration pattern.

**Data structure:** Stack
**Python implementation:** `list`
**Optimal for shortest paths:** No
**Considers weights:** No

DFS may find a path that is longer than the shortest possible route.

---

### 3. Dijkstra's Algorithm

Dijkstra's algorithm is designed for graphs where different edges or cells can have different costs.

In this visualizer:

* Normal cells cost **1**
* Weighted cells cost **5**

Dijkstra's algorithm uses a **min-heap / priority queue** to always process the cell with the lowest known cumulative cost.

```python
heapq.heappop(heap)
```

This allows Dijkstra's to find the **lowest-cost path**, rather than simply the path with the fewest steps.

For example, it may choose:

```text
Short path:
Start → 🟧 → 🟧 → 🟧 → End
Cost = 17
```

instead of:

```text
Longer path:
Start → ⬜ → ⬜ → ⬜ → ⬜ → ⬜ → End
Cost = 6
```

**Data structure:** Min-heap / Priority Queue
**Python implementation:** `heapq`
**Optimal for weighted graphs:** Yes, with non-negative costs
**Considers weights:** Yes

---

## 🔬 Algorithm Comparison

| Algorithm    | Data Structure | Weighted Cells | Shortest Path | Main Behavior                         |
| ------------ | -------------- | -------------: | ------------: | ------------------------------------- |
| **BFS**      | FIFO Queue     |              ❌ |             ✅ | Explores outward layer by layer       |
| **DFS**      | LIFO Stack     |              ❌ |             ❌ | Dives deep before backtracking        |
| **Dijkstra** | Min-Heap       |              ✅ |             ✅ | Prioritizes lowest cumulative cost    |

The project demonstrates an important lesson:

> **Changing the data structure can fundamentally change how an algorithm explores a graph.**

BFS and DFS can use almost identical traversal logic, but replacing a **queue with a stack** produces a completely different exploration pattern.

Similarly, Dijkstra's priority queue allows the algorithm to account for weighted cells, something BFS cannot do.

---

## 🖥️ How the Visualizer Works

The application represents the maze as a **25 × 25 two-dimensional grid**.

Each cell has a state:

```python
EMPTY = 0
WALL = 1
START = 2
END = 3
WEIGHTED = 4
```

The application stores these states in a 2D list:

```python
grid_data = [
    [EMPTY, EMPTY, WALL, EMPTY, ...],
    [EMPTY, WALL, WALL, EMPTY, ...],
    ...
]
```

A second 2D list stores the Tkinter rectangle IDs:

```python
rect_ids
```

These IDs allow the application to update the visual appearance of individual cells using:

```python
canvas.itemconfig(...)
```

This creates a separation between:

1. **The logical state of the grid**
2. **The visual representation of the grid**

---

## 🎨 Cell Colors

| Cell Type | Color      | Meaning                    |
| --------- | ---------- | -------------------------- |
| Empty     | White      | Normal traversable cell    |
| Wall      | Black      | Cannot be traversed        |
| Start     | Green      | Starting position          |
| End       | Red        | Destination                |
| Weighted  | Orange     | Higher traversal cost      |
| Visited   | Light Blue | Cell explored by algorithm |
| Path      | Yellow     | Final path found           |

---

## 🖱️ Controls

### Left Click

Click an empty cell to create a wall.

Click an existing wall to remove it.

### Left Click + Drag

Drag across the grid to continuously draw walls.

### CTRL + Click

* First CTRL + Click → Set the **start** cell
* Second CTRL + Click → Set the **end** cell

### `W` Key

Hover over an empty cell and press `W` to toggle it between:

* Normal cell
* Weighted cell

### Algorithm Buttons

* **BFS** — Run Breadth-First Search
* **DFS** — Run Depth-First Search
* **Dijkstra** — Run Dijkstra's algorithm

### Reset

Removes algorithm visualization while keeping:

* Walls
* Start point
* End point
* Weighted cells

### Clear All

Resets the entire grid.

---

## 🛠️ Technologies Used

* **Python**
* **Tkinter** — Desktop GUI and canvas rendering
* **collections.deque** — BFS queue
* **heapq** — Dijkstra's priority queues

No external cloud services, APIs, or paid resources are required.

---

## 📂 Project Structure

The project is intentionally lightweight:

```text
pathfinder/
│
├── pathfinder.py
└── README.md
```

The main application is contained in:

```text
pathfinder.py
```

---

## 🚀 Getting Started

### Run the Application

Clone or download the project, then run:

```bash
python pathfinder.py
```

The application should open a window containing the interactive pathfinding grid.

---

## 🧪 Suggested Experiment

To compare the algorithms effectively:

### Step 1 — Create a Maze

Use left-click and drag to draw several walls.

### Step 2 — Set Start and End

CTRL+click once to create the green start point.

CTRL+click again to create the red end point.

### Step 3 — Run an Algorithm

Observe how the search spreads outward in even layers.

### Step 4 — Reset

Click **Reset** to remove the exploration visualization while keeping your maze.

### Run Another Algorithm and compare the path lengths

---

## 📚 Key Concepts Learned

This project provided practical experience with several important programming and computer science concepts.

### Graph Representation

A 2D grid can be treated as a graph:

* Each cell is a **node**
* Adjacent cells are connected by **edges**

### Queues

BFS uses a FIFO queue:

```text
First In → First Out
```

This creates broad, layer-by-layer exploration.

### Stacks

DFS uses a LIFO stack:

```text
Last In → First Out
```

This causes the algorithm to explore deeply along individual paths.

### Priority Queues

Dijkstra's uses a min-heap to prioritize the most promising or lowest-cost cells.

### Cost Tracking

Dijkstra's maintains a dictionary such as:

```python
total_cost
```

This records the cheapest known cost to reach each cell.

The following condition determines whether a newly discovered route is worth keeping:

```python
if neighbor not in total_cost or new_cost < total_cost[neighbor]:
```

In plain English:

> "Have we never reached this cell before, or did we just find a cheaper way to reach it?"

### Path Reconstruction

The `came_from` dictionary records where each cell was discovered from.

Once the destination is reached, the algorithm can trace backward from the end to the start and reconstruct the final path.

---

## 💡 Key Takeaways

The biggest lesson from this project is that **algorithm behavior is closely connected to the data structure used to manage the search**.

### BFS

> "Explore everything nearby before going farther."

Uses a queue.

### DFS

> "Follow one path as deeply as possible."

Uses a stack.

### Dijkstra

> "Always explore the cheapest option available."

Uses a priority queue.

---

## 🏆 Project Outcome

By completing this project, I built an interactive application that demonstrates three major pathfinding algorithms:

* **BFS** using a FIFO queue
* **DFS** using a LIFO stack
* **Dijkstra's** using a min-heap

The visualizer makes it possible to directly compare how these algorithms explore the same grid and how their underlying data structures influence their behavior.

---

## 📸 Demo
Coming soon

---

## 👤 Shoutouts

**Abishek Anil**

Built as part of the **NextWork — Build a Pathfinding Algorithm Visualizer** project.
