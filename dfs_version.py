
# Maze Escape - DAA Project
# Depth First Search (DFS) with Backtracking

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

visited = set()
visited_count = 0
path = []


def dfs(row, col):
    global visited_count

    # Check boundaries
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return False

    # Skip walls and visited cells
    if maze[row][col] == "#" or (row, col) in visited:
        return False

    # Mark cell as visited
    visited.add((row, col))
    visited_count += 1
    path.append((row, col))

    # Check destination
    if (row, col) == end:
        return True

    # Explore down, right, up, and left
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for dr, dc in directions:
        if dfs(row + dr, col + dc):
            return True

    # Backtrack
    path.pop()
    return False


if dfs(start[0], start[1]):
    print("Path found using DFS!")
    print("Cells visited by DFS:", visited_count)
    print("Path:", path)

    print("\nMaze with DFS path:")

    for r in range(rows):
        for c in range(cols):
            if (r, c) in path and maze[r][c] not in ("S", "E"):
                print("*", end=" ")
            else:
                print(maze[r][c], end=" ")
        print()
else:
    print("No path found!")
    print("Cells visited by DFS:", visited_count)
