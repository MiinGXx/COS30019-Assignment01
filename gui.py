import tkinter as tk
from grid import create_grid, create_yellow_square
from searchstrategy import dfs_search_store_moves

def create_grid_window(rows, cols, marker, goals, walls):
    """Create and display the Tkinter GUI window with grid, and visualize DFS navigation."""
    window = tk.Tk()
    window.title("Grid Visualization")

    # Create canvas for grid
    canvas = tk.Canvas(window, width=cols * 50, height=rows * 50)
    canvas.pack()

    # Create and display the grid
    create_grid(canvas, rows, cols, markers=[marker], goals=goals, walls=walls)

    # Create the yellow square on top of the marker cell
    yellow_square = create_yellow_square(canvas, marker[0], marker[1])

    def update_square(new_pos):
        """Update the yellow square's position visually on the canvas."""
        cell_size = 50
        square_size = 30  # Smaller size for the yellow square
        x1 = new_pos[0] * cell_size + (cell_size - square_size) / 2
        y1 = new_pos[1] * cell_size + (cell_size - square_size) / 2
        x2 = x1 + square_size
        y2 = y1 + square_size
        # Move the yellow square to the new position
        canvas.coords(yellow_square, x1, y1, x2, y2)
        canvas.tag_raise(yellow_square)  # Ensure the yellow square stays on top
        window.update()  # Update the canvas to reflect the changes

    def highlight_exploring_node(pos):
        """Highlight the currently exploring cell and animate the yellow square."""
        col, row = pos
        cell_size = 50
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        
        # Animate the yellow square movement
        update_square(pos)
        
        # Highlight the cell being explored
        canvas.create_rectangle(x1, y1, x2, y2, fill="lightgreen", outline="black")
        canvas.tag_raise(yellow_square)  # Ensure the yellow square stays on top
        window.update()  # Update the GUI
        window.after(200)  # Delay for animation

    def highlight_visited_node(pos):
        """Highlight the visited node in light blue."""
        col, row = pos
        cell_size = 50
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="black")
        window.update()  # Update the GUI

    # Retrieve the full move history using DFS
    move_history = dfs_search_store_moves(marker, goals, walls, rows, cols,
                                          explore_callback=highlight_exploring_node,
                                          visit_callback=highlight_visited_node)

    # Function to animate the yellow square movement along the final path
    def animate_path(path):
        """Animate the yellow square along the final path to the goal."""
        for pos in path:
            update_square(pos)
            window.after(500)  # Pause for 500ms between movements

    # Automatically animate the yellow square following the final path to the goal
    final_path = move_history[-1][1]  # Get the moves of the final path
    window.after(1000, lambda: animate_path([pos for pos, moves in move_history]))

    window.mainloop()
