
# Maze Escape - DAA Project
# Finding a path using DFS

maze = [
    ["S", ".", "#", ".", "."],
    ["#", ".", "#", ".", "#"],
    [".", ".", ".", ".", "#"],
    [".", "#", "#", ".", "."],
    [".", ".", ".", "#", "E"]
]

rows = len(maze)
cols = len(maze[0])

# Starting and ending positions
start = (0, 0)
end = (4, 4)

# Store the cells we have visited
visited = set()

# Store the final path
path = []


def dfs(row, col):
    # Check if the position is outside the maze
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return False

    # Stop if the cell is a wall or already visited
    if maze[row][col] == "#" or (row, col) in visited:
        return False

    # Mark the cell as visited
    visited.add((row, col))
    path.append((row, col))

    # Check if we reached the destination
    if (row, col) == end:
        return True

    # Explore down, right, up, and left
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for dr, dc in directions:
        if dfs(row + dr, col + dc):
            return True

    # Backtrack if no path works from this cell
    path.pop()
    return False


if dfs(start[0], start[1]):
    print("Path found!")
    print(path)

    # Display the maze with the path
    for r in range(rows):
        for c in range(cols):
            if (r, c) in path and maze[r][c] not in ("S", "E"):
                print("*", end=" ")
            else:
                print(maze[r][c], end=" ")
        print()
else:
    print("No path found!")
