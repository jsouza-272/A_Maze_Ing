*This project has been created as part of the 42 curriculum by jsouza-272.*

# A-Maze-Ing

## Description

A-Maze-Ing is a Python maze generator that reads a configuration file, generates a (possibly perfect) maze, writes the result to an output file using a hexadecimal wall encoding, and provides an interactive terminal ASCII visual representation.

A **perfect maze** has exactly one path between any two cells (no loops, no isolated regions). The generator uses a Depth-First Search (DFS) backtracker algorithm seeded for reproducibility. Every generated maze embeds a visible **"42" pattern** (when the maze is large enough) as a set of fully closed cells. An A* solver computes the shortest path from entry to exit, which can be shown or hidden in the visual display.

---

## Instructions

### Prerequisites

- **Python 3.10** or later

### How to run

```bash
python3 a_maze_ing.py config.txt
```

- `a_maze_ing.py` is the main program file (name is mandatory).
- `config.txt` is the only argument: a plain-text configuration file (see section below). Any filename is accepted.

### Using the default configuration file

A ready-to-use `config.txt` is provided at the root of the repository:

```bash
python3 a_maze_ing.py config.txt
```

### Error handling

The program handles all errors gracefully and never crashes unexpectedly. On any error (missing file, bad syntax, invalid values, impossible parameters, etc.) it prints a clear message and exits cleanly.

---

## Configuration file format

The configuration file uses one `KEY=VALUE` pair per line. Lines starting with `#` are comments and are ignored. Blank lines are also ignored.

### Mandatory keys

| Key           | Description                                    | Example                  |
|---------------|------------------------------------------------|--------------------------|
| `WIDTH`       | Maze width in number of cells                  | `WIDTH=20`               |
| `HEIGHT`      | Maze height in number of cells                 | `HEIGHT=15`              |
| `ENTRY`       | Entry cell coordinates as `x,y`                | `ENTRY=0,0`              |
| `EXIT`        | Exit cell coordinates as `x,y`                 | `EXIT=19,14`             |
| `OUTPUT_FILE` | Path to the output file                        | `OUTPUT_FILE=maze.txt`   |
| `PERFECT`     | Generate a perfect maze (`True` or `False`)    | `PERFECT=True`           |

### Optional keys

| Key         | Description                                              | Example           |
|-------------|----------------------------------------------------------|-------------------|
| `SEED`      | Integer seed for reproducible random generation          | `SEED=42`         |
| `ALGORITHM` | Generation algorithm (currently only `dfs` is supported) | `ALGORITHM=dfs`   |

### Example configuration file

```ini
# A-Maze-Ing configuration file
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
# Optional: fix the random seed for reproducibility
# SEED=42
```

---

## Output file format

Each cell is represented by **one hexadecimal digit** that encodes which walls are closed. Cells are stored row by row, one row per line.

### Bit mapping

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1       | East  |
| 2       | South |
| 3       | West  |

A bit set to `1` means the wall is **closed** (present); `0` means **open** (passage).

**Example:** `3` → binary `0011` → North and East walls closed.  
**Example:** `A` → binary `1010` → East and West walls closed.

### Structure of the output file

1. The hexadecimal maze — one row per line, each character is a hex digit for one cell.
2. An empty line.
3. Entry coordinates: `x, y`
4. Exit coordinates: `x, y`
5. Shortest path from entry to exit as a sequence of cardinal letters: `N`, `E`, `S`, `W`

All lines end with `\n`.

### Example output snippet

```
f9ebb...
fe8db...
...

0, 0
19, 14
EESSEENN...
```

---

## Maze generation algorithm

The maze is generated using the **Depth-First Search (DFS) recursive backtracker** algorithm (implemented in `mazegen/algorithms/Dfs.py`).

**Why DFS?**

- It naturally produces a **perfect maze** (a spanning tree of the grid graph), with exactly one path between any two cells, by carving passages without revisiting cells.
- It is straightforward to implement and to seed for reproducibility.
- It creates mazes with long, winding corridors — visually interesting and easy to verify.
- To generate an **imperfect maze** (when `PERFECT=False`), the DFS pass is run a second time on partially visited cells to add extra passages (loops), while still maintaining full connectivity.

The shortest path from entry to exit is found using the **A* algorithm** with Manhattan distance as the heuristic (`mazegen/algorithms/Astar.py`).

---

## Reusable module

The maze generation logic is encapsulated in the `MazeGenerator` class inside the `mazegen` package. This package can be imported into any Python project and is distributed as a standalone wheel/tarball.

### Installation

From the root of the repository:

```bash
pip install dist/mazegen-0.1.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen import MazeGenerator, Astar

# Instantiate the generator
gen = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    output_file="maze.txt",
    perfect=True,
    seed=42          # optional: omit for a random maze
)

# Generate and save the maze
gen.generate_maze()
gen.save_maze()

# Access the hex representation
hex_maze: str = gen.get_maze()

# Access the maze structure (grid of Cell objects)
maze_grid = gen.maze          # gen.maze is a Maze instance
                               # maze_grid.maze[y][x] is a Cell

# Solve the maze
path = Astar().algorithm(gen.maze, (0, 0), (19, 14))
# path is a list of (x, y) tuples representing the solution

# Get the cardinal-direction string (N/E/S/W)
cardinal = Astar.make_cardinal_path(path.copy(), (19, 14))
print(cardinal)  # e.g. "EESSENN..."
```

### Custom parameters

| Parameter    | Type             | Default | Description                              |
|--------------|------------------|---------|------------------------------------------|
| `width`      | `int`            | —       | Number of columns                        |
| `height`     | `int`            | —       | Number of rows                           |
| `entry`      | `tuple[int,int]` | —       | Entry cell (x, y)                        |
| `exit`       | `tuple[int,int]` | —       | Exit cell (x, y)                         |
| `output_file`| `str`            | —       | Output file path                         |
| `perfect`    | `bool`           | —       | `True` for a perfect maze, `False` for loops |
| `seed`       | `int | None`     | `None`  | RNG seed for reproducibility             |

### Accessing the maze structure and solution

- `gen.maze` — a `Maze` instance; `gen.maze.maze[y][x]` returns a `Cell` with `._walls` dict (`'N'`, `'E'`, `'S'`, `'W'` → `bool`).
- `gen.get_maze()` — returns the full hex string of the maze (same format as the output file).
- `Astar().algorithm(maze, entry, exit)` — returns a `list[tuple[int,int]]` of cell coordinates on the shortest path.
- `Astar.make_cardinal_path(path, exit)` — converts the coordinate list to a `str` of `N`/`E`/`S`/`W` characters.

### Building the package

All source files needed to rebuild the package are included in the repository. To rebuild in a clean virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install build
python -m build
# Produces dist/mazegen-*.whl and dist/mazegen-*.tar.gz
```

The pre-built artifacts (`mazegen-0.1.0-py3-none-any.whl` and `mazegen-0.1.0.tar.gz`) are available in the `dist/` directory at the root of the repository.

---

## Visual representation

The program provides an **interactive terminal ASCII** display using ANSI color codes. The maze is rendered with Unicode block characters (`█`) for walls and colored cells for the entry, exit, and solution path.

### How to interact

After the maze is generated, an interactive menu is shown in the terminal:

```
=== A-Maze-Ing ===
1. Re-generate a new maze
2. Show path from entry to exit (False)
3. Rotate maze colors
0. Quit

Choice (0-3):
```

| Key / Input | Action                                           |
|-------------|--------------------------------------------------|
| `1`         | Re-generate a new random maze and display it     |
| `2`         | Toggle showing / hiding the shortest path        |
| `3`         | Cycle maze wall color (white ↔ 42 yellow)        |
| `0`         | Quit the program                                 |

### Color coding

| Color         | Meaning             |
|---------------|---------------------|
| White / yellow | Maze walls (toggleable) |
| Blue           | Entry cell          |
| Red            | Exit cell           |
| Green          | Shortest path cells |
| Grey           | "42" pattern cells  |

**Note:** MLX graphical display is not implemented in this version. All visualization is done in the terminal.

**TODO (optional):** Dedicated key binding to highlight/un-highlight the "42" pattern with a custom color.

---

## Team & project management

This is a solo project. All roles were handled by the same student:

- **Architecture & design** — defining module boundaries (`mazegen`, `parser`, `Ui`)
- **Algorithm implementation** — DFS backtracker for generation, A\* for solving
- **Configuration & parsing** — full validation pipeline with clear error messages
- **Output serialization** — hex encoding, entry/exit/path format
- **Terminal UI** — ANSI rendering, interactive menu
- **Packaging** — `pyproject.toml`, wheel + tarball via `python -m build`
- **Documentation** — docstrings (Google style), README

### Planning

The project was planned around the mandatory spec sections (config → generation → output → visual → packaging) worked through in order. Incremental testing was used after each module was added.

### What worked well

- The DFS algorithm integrated cleanly with the `Maze` / `Cell` object model.
- Using `try`/`except` with typed custom errors (`FtError`, `AstarError`) kept error paths explicit.
- Separating generation logic into a standalone package made the reusability requirement straightforward.

### Improvements

- MLX graphical rendering was not implemented; a future version could add it.
- The "42" bitmap selection could be extended to more maze sizes.

### Tools used

- **Python 3.10+** — main language
- **flake8** — linting
- **mypy** — static type checking
- **pytest** — unit testing
- **build / poetry** — packaging

---

## Resources

### References

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Randomized depth-first search (recursive backtracker)](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search)
- [Prim's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm) — alternative spanning-tree approach
- [A* search algorithm — Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Graph theory and spanning trees](https://en.wikipedia.org/wiki/Spanning_tree)
- [Python 3.10 documentation](https://docs.python.org/3.10/)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [mypy documentation](https://mypy.readthedocs.io/)

### AI usage

AI assistance (ChatGPT / GitHub Copilot) was used for the following tasks during this project:

- **Boilerplate generation** — initial scaffolding for the `pyproject.toml` and `Makefile` rules.
- **Docstring drafting** — generating first-pass Google-style docstrings that were then reviewed and corrected.
- **Debugging suggestions** — explaining cryptic mypy or flake8 errors and proposing fixes.
- **README structure** — suggesting section ordering and Markdown formatting, then manually reviewed and rewritten to match the actual implementation.

All AI-generated content was reviewed, tested, and validated before being included. No code was accepted without full understanding of its behavior.
