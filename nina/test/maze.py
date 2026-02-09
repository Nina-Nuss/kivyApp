import random

def create_maze(w, h):
    # Initialize grid with walls (1)
    maze = [[1] * w for _ in range(h)]
    visited = set()
    def walk(x, y):
        maze[y][x] = 0  # Mark path
        visited.add((x, y)) 
        # Directions: North, South, East, West
        neighbors = [(x-2, y), (x+2, y), (x, y-2), (x, y+2)]
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                # Remove wall between current and neighbor
                maze[(y + ny) // 2][(x + nx) // 2] = 0
                walk(nx, ny)
    walk(0, 0)
    return maze

# Print the maze
# Using "#" instead of "█" for better compatibility with Windows terminals (cp1252)
for row in create_maze(21, 11):
    print("".join("#" if cell else " " for cell in row))
