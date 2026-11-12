
# Maze Escape - DAA Project
# Breadth First Search (BFS)

from collections import deque

maze = [
    ["S", ".", "#", ".", "."],
    ["#", ".", "#", ".", "#"],
    [".", ".", ".", ".", "#"],
    [".", "#", "#", ".", "."],
    [".", ".", ".", "#", "E"]
]

rows = len(maze)
cols = len(maze[0])

start = (0, 0)
end = (4, 4)

queue = deque([start])
visited = {start}
visited_count = 1
parent = {start: None}

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

while queue:
    row, col = queue.popleft()

    # Stop when destination is reached
    if (row, col) == end:
        break

    # Explore neighboring cells
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        next_cell = (new_row, new_col)

        # Check boundaries
        if not (0 <= new_row < rows and 0 <= new_col < cols):
            continue

        # Skip walls and visited cells
        if maze[new_row][new_col] == "#" or next_cell in visited:
            continue

        visited.add(next_cell)
        visited_count += 1
        parent[next_cell] = (row, col)
        queue.append(next_cell)

# Reconstruct shortest path
path = []

if end in parent:
    current = end

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    print("Shortest path found using BFS!")
    print("Cells visited by BFS:", visited_count)
    print("Path:", path)

    print("\nMaze with BFS path:")

    for r in range(rows):
        for c in range(cols):
            if (r, c) in path and maze[r][c] not in ("S", "E"):
                print("*", end=" ")
            else:
                print(maze[r][c], end=" ")
        print()
else:
    print("No path found!")
    print("Cells visited by BFS:", visited_count)
