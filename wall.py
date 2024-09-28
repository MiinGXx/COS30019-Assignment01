def add_wall_coordinates(start_col, start_row, width, height):
    """Helper function to calculate all the coordinates occupied by a wall."""
    wall_coords = []
    for row in range(start_row, start_row + height):
        for col in range(start_col, start_col + width):
            wall_coords.append((col, row))
    return wall_coords
