from src.template.CustomWidgets.MapWidget import Map


def method(original_map: Map, fill_probability=0.55, smoothing_iterations=6) -> Map:
    """
    Generates a dungeon-like map using cellular automata.

    - Walls surround the map.
    - Floors appear with some obstacles like lava and spikes.

    :param original_map: The original Map object.
    :param fill_probability: Probability of a cell being a wall.
    :param smoothing_iterations: Number of smoothing steps.
    :return: A new dungeon-style Map.
    """
    import copy
    import random

    rows, cols = original_map.row_number, original_map.column_number
    x, y = original_map.x, original_map.y
    original_map = Map(original_map.project_name, original_map.save_file_name, rows, cols, original_map.tile_size)
    original_map.x = x
    original_map.y = y
    # Step 1: Create a new map with the same properties as the original map
    new_map = copy.deepcopy(original_map)
    new_map.tiles_coordinates_by_name.clear()

    # Initialize map with walls and floors
    grid = [[1 if random.random() < fill_probability else 0 for _ in range(cols)] for _ in range(rows)]

    def count_neighbors(grid, x, y):
        count = sum(1 for dx, dy in [(-1, -1), (-1, 0), (-1, 1),
                                     (0, -1),         (0, 1),
                                     (1, -1), (1, 0), (1, 1)]
                    if 0 <= x + dx < rows and 0 <= y + dy < cols and grid[x + dx][y + dy] == 1)
        return count

    for _ in range(smoothing_iterations):
        new_grid = [[0] * cols for _ in range(rows)]
        for x in range(rows):
            for y in range(cols):
                neighbors = count_neighbors(grid, x, y)
                if grid[x][y] == 1:
                    new_grid[x][y] = 1 if neighbors >= 4 else 0
                else:
                    new_grid[x][y] = 1 if neighbors >= 5 else 0
        grid = new_grid

    # Add obstacles
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == 0 and random.random() < 0.05:  # 5% chance for obstacles
                grid[x][y] = 2 if random.random() < 0.5 else 3  # Lava or Spikes

    # Convert grid into dungeon tiles
    terrain_types = {
        0: "Floor.png",
        1: "Wall.png",
        2: "Lava.png",
        3: "Door (manmade tunnel).png"
    }

    for x in range(rows):
        for y in range(cols):
            tile_type = terrain_types[grid[x][y]]
            if tile_type not in new_map.tiles_coordinates_by_name:
                new_map.tiles_coordinates_by_name[tile_type] = []
            new_map.tiles_coordinates_by_name[tile_type].append((y, x))

    return new_map

