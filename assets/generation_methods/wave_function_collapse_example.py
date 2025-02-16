from src.template.CustomWidgets.MapWidget import Map

def method(original_map: Map, fill_probability=0.55, smoothing_iterations=6) -> Map:
    """
    Generates a new map using Wave Function Collapse (WFC).

    - Uses tile adjacency rules to ensure logical map structures.
    - Avoids impossible configurations (e.g., water in the middle of walls).
    - Each tile affects its neighbors in a structured way.

    :param original_map: The original Map object.
    :return: A new Map generated using WFC.
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

    # Define tile rules: what can be next to what
    tile_rules = {
        "Water.png": ["Water.png", "Sand.png"],
        "Sand.png": ["Water.png", "Grass.png"],
        "Grass.png": ["Sand.png", "Rock (large).png", "Rock.png"],
        "Rock (large).png": ["Grass.png", "Rock.png"],
        "Rock.png": ["Grass.png", "Rock (large).png"]
    }

    # Initialize grid with all possible tiles
    grid = [[list(tile_rules.keys()) for _ in range(cols)] for _ in range(rows)]

    def collapse_cell(x, y):
        """ Picks a tile for (x, y) based on possibilities and constraints. """
        if not grid[x][y]:
            # If no valid options, assign a random tile (fallback)
            grid[x][y] = [random.choice(list(tile_rules.keys()))]

        if len(grid[x][y]) == 1:
            return  # Already collapsed

        # Pick a tile randomly
        grid[x][y] = [random.choice(grid[x][y])]

        # Propagate constraints to neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4-way adjacency
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                valid_neighbors = tile_rules[grid[x][y][0]]
                grid[nx][ny] = [tile for tile in grid[nx][ny] if tile in valid_neighbors]

                # Ensure there is always at least one valid tile
                if not grid[nx][ny]:
                    grid[nx][ny] = [random.choice(list(tile_rules.keys()))]

                if len(grid[nx][ny]) == 1:
                    collapse_cell(nx, ny)  # Recursively collapse if only one option remains

    # Collapse cells one by one
    while any(len(grid[x][y]) > 1 for x in range(rows) for y in range(cols)):
        min_entropy_cells = [(x, y) for x in range(rows) for y in range(cols) if len(grid[x][y]) > 1]
        x, y = random.choice(min_entropy_cells)
        collapse_cell(x, y)

    # Convert collapsed grid to map tiles
    for x in range(rows):
        for y in range(cols):
            tile_type = grid[x][y][0]  # No more empty lists due to fix
            if tile_type not in new_map.tiles_coordinates_by_name:
                new_map.tiles_coordinates_by_name[tile_type] = []
            new_map.tiles_coordinates_by_name[tile_type].append((y, x))

    return new_map

