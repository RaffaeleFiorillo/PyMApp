from src.template.CustomWidgets.MapWidget import Map

def method(original_map: Map, fill_probability=0.35, smoothing_iterations=4) -> Map:
    """
    Generates an island-like map using cellular automata.

    - Water (default) fills the map.
    - Higher areas become Sand, Grass, or Rock based on height.

    :param original_map: The original Map object.
    :param fill_probability: Probability (0-1) of land appearing initially.
    :param smoothing_iterations: Number of smoothing steps.
    :return: A new Map with an island effect.
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

    # Initialize with water and some land
    grid = [[1 if random.random() < fill_probability else 0 for _ in range(cols)] for _ in range(rows)]

    def count_neighbors(grid, x, y):
        neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1),
                            (0, -1),         (0, 1),
                            (1, -1), (1, 0), (1, 1)]
        count = sum(1 for dx, dy in neighbor_offsets if 0 <= x + dx < rows and 0 <= y + dy < cols and grid[x + dx][y + dy] == 1)
        return count

    for _ in range(smoothing_iterations):
        new_grid = [[0] * cols for _ in range(rows)]
        for x in range(rows):
            for y in range(cols):
                neighbors = count_neighbors(grid, x, y)
                new_grid[x][y] = 1 if neighbors >= 4 else 0
        grid = new_grid

    # Convert grid into island terrain types
    terrain_types = {
        0: "Water.png",
        1: "Sand.png",
        2: "Grass.png",
        3: "Rock.png"
    }

    for x in range(rows):
        for y in range(cols):
            land_value = sum(1 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if 0 <= x + dx < rows and 0 <= y + dy < cols and grid[x + dx][y + dy] == 1)
            terrain = terrain_types[min(land_value, 3)]  # Pick tile type based on neighbor count
            if terrain not in new_map.tiles_coordinates_by_name:
                new_map.tiles_coordinates_by_name[terrain] = []
            new_map.tiles_coordinates_by_name[terrain].append((y, x))

    return new_map
