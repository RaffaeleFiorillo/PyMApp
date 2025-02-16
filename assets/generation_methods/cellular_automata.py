import random
import copy
from src.template.CustomWidgets.MapWidget import Map


def method(original_map: Map, fill_probability=0.45, smoothing_iterations=5) -> Map:
    """
    Generates a new map using cellular automata based on an existing Map object.

    :param original_map: The original Map object.
    :param fill_probability: Probability (0-1) that a cell starts as a wall.
    :param smoothing_iterations: Number of iterations to smooth the terrain.
    :return: A new Map object with terrain generated using cellular automata.
    """

    rows, cols = original_map.row_number, original_map.column_number
    x, y = original_map.x, original_map.y
    original_map = Map(original_map.project_name, original_map.save_file_name, rows, cols, original_map.tile_size)
    original_map.x = x
    original_map.y = y
    # Step 1: Create a new map with the same properties as the original map
    new_map = copy.deepcopy(original_map)
    new_map.tiles_coordinates_by_name.clear()

    # Step 2: Initialize the grid randomly
    grid = [[1 if random.random() < fill_probability else 0 for _ in range(cols)] for _ in range(rows)]

    def count_neighbors(grid, x, y):
        """Counts the number of wall neighbors around a given cell."""
        neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1),
                            (0, -1), (0, 1),
                            (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in neighbor_offsets:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                count += grid[nx][ny]  # Count walls
            else:
                count += 1  # Treat out-of-bounds as walls
        return count

    # Step 3: Apply cellular automata rules for smoothing
    for _ in range(smoothing_iterations):
        new_grid = [[0] * cols for _ in range(rows)]
        for x in range(rows):
            for y in range(cols):
                neighbors = count_neighbors(grid, x, y)
                if grid[x][y] == 1:  # If it's a wall
                    new_grid[x][y] = 1 if neighbors >= 4 else 0
                else:  # If it's empty space
                    new_grid[x][y] = 1 if neighbors >= 5 else 0
        grid = new_grid

    # Step 4: Convert grid to tile coordinates
    wall_tile_name = "Boulder.png"
    floor_tile_name = "Floor.png"

    for x in range(rows):
        for y in range(cols):
            tile_type = wall_tile_name if grid[x][y] == 1 else floor_tile_name
            if tile_type not in new_map.tiles_coordinates_by_name:
                new_map.tiles_coordinates_by_name[tile_type] = []
            new_map.tiles_coordinates_by_name[tile_type].append((y, x))  # (col, row)

    return new_map