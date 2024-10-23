import tkinter as tk
from grid import create_grid, create_yellow_square, animate_path
from searchstrategy import dfs, bfs, gbfs, a_star, highlight_final_path, new_render_search_tree_tk

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

def create_grid_window(rows, cols, marker, goals, walls, method, cell_size=50):
    window = tk.Tk()
    window.title("Grid and Search Tree Visualization")

    # Configure grid layout to allow dynamic scaling
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    # Canvas for grid visualization
    grid_canvas = tk.Canvas(window, width=cols * cell_size, height=rows * cell_size)
    grid_canvas.grid(row=0, column=0, sticky="nsew")

    # Canvas for search tree visualization (scalable with window resizing)
    tree_canvas = tk.Canvas(window, bg="white")
    tree_canvas.grid(row=0, column=1, sticky="nsew", padx=20)

    # Make the canvas scrollable
    hbar = tk.Scrollbar(window, orient=tk.HORIZONTAL, command=tree_canvas.xview)
    hbar.grid(row=1, column=1, sticky='ew')
    vbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=tree_canvas.yview)
    vbar.grid(row=0, column=2, sticky='ns')
    tree_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    
    add_zoom_and_pan(tree_canvas)  # Add zoom and pan to the search tree canvas

    create_grid(grid_canvas, rows, cols, markers=[marker], goals=goals, walls=walls)

    # Run the selected search algorithm
    if method == "DFS":
        path, node_count, directions, parent = dfs(marker, goals, walls, rows, cols, grid_canvas, cell_size, tree_canvas)
    elif method == "BFS":
        path, node_count, directions, parent = bfs(marker, goals, walls, rows, cols, grid_canvas, cell_size, tree_canvas)
    elif method == "GBFS":
        path, node_count, directions, parent = gbfs(marker, goals, walls, rows, cols, grid_canvas, cell_size, tree_canvas)
    elif method == "AS":
        path, node_count, directions, parent = a_star(marker, goals, walls, rows, cols, grid_canvas, cell_size, tree_canvas)
    else:
        print(f"Method '{method}' not supported.")
        return

    if path:
        highlight_final_path(grid_canvas, path, cell_size)
        yellow_square = create_yellow_square(grid_canvas, marker[0], marker[1], cell_size)
        animate_path(grid_canvas, yellow_square, path)

        # Render the final search tree (if needed)
        new_render_search_tree_tk(parent, tree_canvas)

    window.mainloop()