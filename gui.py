import tkinter as tk
from grid import create_grid, create_yellow_square, animate_path, move_yellow_square
from searchstrategy import dfs, bfs, gbfs, a_star, iddfs, weighted_astar, highlight_final_path, highlight_cell
from search_tree import render_search_tree

# Global variables for storing the current state
state = {
    "steps": [],
    "yellow_square": None,
    "current_step": -1,
    "search_completed": False  # To track when the search is complete
}

def add_zoom_and_pan(canvas):
    """Add zoom and pan functionality to the canvas."""
    scale = 1.0
    start_x = start_y = 0

    def on_mouse_wheel(event):
        nonlocal scale
        # Zoom in or out depending on the scroll direction
        if event.delta > 0:  # Scroll up -> Zoom in
            scale = 1.1
        elif event.delta < 0:  # Scroll down -> Zoom out
            scale = 0.9
        canvas.scale("all", event.x, event.y, scale, scale)  # Scale around the mouse pointer
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_button_press(event):
        nonlocal start_x, start_y
        # Store the initial mouse position when the drag starts
        start_x = event.x
        start_y = event.y

    def on_mouse_drag(event):
        # Calculate the amount of movement and scroll accordingly
        dx = start_x - event.x  # Invert the direction of x movement
        dy = start_y - event.y  # Invert the direction of y movement
        canvas.scan_dragto(int(-dx), int(-dy), gain=1)

    # Bind events for zooming and panning
    canvas.bind("<MouseWheel>", on_mouse_wheel)  # Zoom on scroll (Windows/Linux)
    canvas.bind("<ButtonPress-1>", on_button_press)  # Start dragging on left click
    canvas.bind("<B1-Motion>", on_mouse_drag)  # Drag the canvas on left click

def next_step(canvas, tree_canvas, rows, cols, marker, goals, walls, cell_size):
    """Advance one step in the search process, resetting if necessary."""
    global state
    # If the search is completed and we're at the end of steps, reset the grid first
    if state["search_completed"] and state["current_step"] == -1:
        # Reset the grid visualizer
        reset_grid(canvas, tree_canvas, rows, cols, marker, goals, walls, cell_size)

    # Check if there are more steps available
    while state["current_step"] < len(state["steps"]) - 1:
        state["current_step"] += 1  # Move one step forward
        step = state["steps"][state["current_step"]]

        if step[0] == 'move':
            # Move the yellow square to the next cell
            move_yellow_square(canvas, state["yellow_square"], step[1][0], step[1][1], cell_size)
            canvas.update()  # Ensure the move is immediately rendered
            break  # Break after a visible action
        
        elif step[0] == 'highlight':
            # Highlight the next node
            highlight_cell(canvas, step[1], cell_size, step[2])  # Apply the correct highlight color
            # Also move the yellow square during node exploration
            move_yellow_square(canvas, state["yellow_square"], step[1][0], step[1][1], cell_size)
            canvas.update()  # Ensure both highlight and move are rendered immediately
            break  # Break after a visible action
        
        elif step[0] == 'tree_update':
            # Re-render the search tree for the next step
            render_search_tree(step[1], tree_canvas)
            canvas.update()  # Ensure the tree update is immediately rendered
            # Continue loop, as tree update may not be visually noticeable

def previous_step(canvas, tree_canvas, cell_size):
    """Backtrack one step in the search process."""
    global state
    if state["current_step"] > 0:
        state["current_step"] -= 1  # Move one step back
        step = state["steps"][state["current_step"]]

        if step[0] == 'move':
            # Move the yellow square back to the previous cell
            move_yellow_square(canvas, state["yellow_square"], step[1][0], step[1][1], cell_size)
        
        elif step[0] == 'highlight':
            # Clear the current highlight
            highlight_cell(canvas, step[1], cell_size, "white")  # Reset the highlighted cell
        
        elif step[0] == 'tree_update':
            # Re-render the search tree up to this point
            render_search_tree(step[1], tree_canvas)

        canvas.update()  # Update the canvas after backtracking

def reset_grid(canvas, tree_canvas, rows, cols, marker, goals, walls, cell_size):
    """Reset the grid and search tree canvas, clearing all highlights and returning to the initial state."""
    global state
    # Clear the canvases
    canvas.delete("all")
    tree_canvas.delete("all")

    # Recreate the grid and reset the yellow square
    create_grid(canvas, rows, cols, markers=[marker], goals=goals, walls=walls)
    state["yellow_square"] = create_yellow_square(canvas, marker[0], marker[1], cell_size)

    # Reset the current step counter
    state["current_step"] = -1

    # Update the canvas after reset
    canvas.update()
    tree_canvas.update()

def create_grid_window(rows, cols, marker, goals, walls, method, weight=None, cell_size=50):
    window = tk.Tk()
    window.title("Grid and Search Tree Visualization")

    # Configure grid layout to allow dynamic scaling
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)  # New row for buttons
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    # Frame for grid visualization with scrollbars
    grid_frame = tk.Frame(window)
    grid_frame.grid(row=0, column=0, sticky="nsew")

    grid_canvas = tk.Canvas(grid_frame, width=cols * cell_size, height=rows * cell_size, bg="white")
    grid_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    grid_hbar = tk.Scrollbar(grid_frame, orient=tk.HORIZONTAL, command=grid_canvas.xview)
    grid_hbar.pack(side=tk.BOTTOM, fill=tk.X)
    grid_vbar = tk.Scrollbar(grid_frame, orient=tk.VERTICAL, command=grid_canvas.yview)
    grid_vbar.pack(side=tk.RIGHT, fill=tk.Y)
    grid_canvas.config(xscrollcommand=grid_hbar.set, yscrollcommand=grid_vbar.set)

    # Text widget for displaying the output information
    output_text = tk.Text(window, height=10, width=50, font=("Arial", 12))
    output_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # Canvas for search tree visualization (scalable with window resizing)
    tree_canvas = tk.Canvas(window, bg="white")
    tree_canvas.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=20)

    # Make the canvas scrollable
    hbar = tk.Scrollbar(window, orient=tk.HORIZONTAL, command=tree_canvas.xview)
    hbar.grid(row=2, column=1, sticky='ew')
    vbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=tree_canvas.yview)
    vbar.grid(row=0, column=2, rowspan=2, sticky='ns')
    tree_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    
    add_zoom_and_pan(tree_canvas)  # Add zoom and pan to the search tree canvas

    def run_search():
        """Run the selected search algorithm and update the visualizations."""
        global state
        # Clear the canvases and output text
        grid_canvas.delete("all")
        tree_canvas.delete("all")
        output_text.delete("1.0", tk.END)

        # Recreate the grid
        create_grid(grid_canvas, rows, cols, markers=[marker], goals=goals, walls=walls)

        # Run the selected search algorithm
        if method == "DFS":
            path, node_count, directions, parent, steps = dfs(marker, goals, walls, rows, cols, grid_canvas, cell_size, tree_canvas)
        elif method == "BFS":
            path, node_count, directions, parent, steps = bfs(marker, goals, walls, rows, cols, grid_canvas, cell_size, tree_canvas)
        elif method == "GBFS":
            path, node_count, directions, parent, steps = gbfs(marker, goals, walls, rows, cols, grid_canvas, cell_size, tree_canvas)
        elif method == "AS":
            path, node_count, directions, parent, steps = a_star(marker, goals, walls, rows, cols, grid_canvas, cell_size, tree_canvas)
        elif method == "IDDFS":
            result = iddfs(marker, goals, walls, rows, cols, grid_canvas, cell_size, tree_canvas)
            if result:
                path, node_count, directions, parent, steps, iteration_count, total_nodes_expanded, final_iteration_nodes = result
                # Display additional metrics specific to IDDFS
                output_text.insert(tk.END, f"Search Strategy: IDDFS\n")
                output_text.insert(tk.END, f"Goal Reached: {path[-1]}\n")
                output_text.insert(tk.END, f"Total Number of Nodes Expanded: {total_nodes_expanded}\n")
                output_text.insert(tk.END, f"Number of Iterations: {iteration_count}\n")
                output_text.insert(tk.END, f"Total Nodes in Final Iteration: {final_iteration_nodes}\n")
                output_text.insert(tk.END, f"Final Path to Goal: {', '.join(directions)}\n")
                return  # Exit function after displaying IDDFS results
        elif method == "WAS":
            path, node_count, directions, parent, steps = weighted_astar(marker, goals, walls, rows, cols, grid_canvas, cell_size, tree_canvas, weight)
        else:
            output_text.insert(tk.END, f"Method '{method}' not supported.\n")
            return

        # If a path was found, highlight the path and update the output for other algorithms
        if path:
            highlight_final_path(grid_canvas, path, cell_size)
            state["yellow_square"] = create_yellow_square(grid_canvas, marker[0], marker[1], cell_size)
            animate_path(grid_canvas, state["yellow_square"], path)

            # Render the final search tree (if needed)
            render_search_tree(parent, tree_canvas)

            # Display the output information for other methods
            goal_reached = path[-1]
            output_text.insert(tk.END, f"Search Strategy: {method}\n")
            output_text.insert(tk.END, f"Goal Reached: {goal_reached}\n")
            output_text.insert(tk.END, f"Number of Nodes to Reach Goal: {node_count}\n")
            output_text.insert(tk.END, f"Final Path to Goal: {', '.join(directions)}\n")

        # Store the steps and initialize step tracking for forward/backward steps
        state["steps"] = steps
        state["current_step"] = -1  # Start before the first step
        state["search_completed"] = True  # Mark the search as completed

    # Frame for buttons
    button_frame = tk.Frame(window)
    button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

    # Button labels and their corresponding commands
    button_commands = {
        "Next Step": lambda: next_step(grid_canvas, tree_canvas, rows, cols, marker, goals, walls, cell_size),
        "Previous Step": lambda: previous_step(grid_canvas, tree_canvas, cell_size),
        "Start Over": run_search
    }

    # Create and add buttons to the frame
    for label, command in button_commands.items():
        button = tk.Button(button_frame, text=label, command=command)
        button.pack(side=tk.LEFT, padx=5)

    # Initial run of the search algorithm
    run_search()

    window.mainloop()