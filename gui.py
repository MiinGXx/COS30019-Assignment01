import tkinter as tk
from grid import create_grid, create_yellow_square, animate_path, highlight_final_path
from searchstrategy import dfs, bfs, gbfs, a_star, iddfs, ida_star

def create_grid_window(rows, cols, marker, goals, walls, method, weight=None, find_multiple_paths=False, cell_size=30):
    window = tk.Tk()
    window.title("Grid Visualization")

    # Canvas for grid visualization
    grid_canvas = tk.Canvas(window, width=cols * cell_size, height=rows * cell_size, bg="white")
    grid_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Text widget for displaying output information
    output_text = tk.Text(window, height=10, width=cols * cell_size // 10, font=("Arial", 12), state=tk.DISABLED)
    output_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Dictionary to map method abbreviations to full names
    method_full_names = {
        "DFS": "Depth-First Search",
        "BFS": "Breadth-First Search",
        "GBFS": "Greedy Best-First Search",
        "AS": "A* Search",
        "CUS1": "Iterative Deepening Depth-First Search",
        "CUS2": "Iterative Deepening A* Search"
    }

    def run_search():
        # Clear the canvas and output text
        grid_canvas.delete("all")
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
    
        # Create the initial grid with the marker, goals, and walls
        create_grid(grid_canvas, rows, cols, markers=[marker], goals=goals, walls=walls)
    
        # Execute the selected search algorithm
        if method == "DFS":
            result = dfs(marker, goals, walls, rows, cols, grid_canvas, cell_size, find_multiple_paths)
        elif method == "BFS":
            result = bfs(marker, goals, walls, rows, cols, grid_canvas, cell_size, find_multiple_paths)
        elif method == "GBFS":
            result = gbfs(marker, goals, walls, rows, cols, grid_canvas, cell_size, find_multiple_paths)
        elif method == "AS":
            result = a_star(marker, goals, walls, rows, cols, grid_canvas, cell_size, find_multiple_paths)
        elif method == "CUS1":
            result = iddfs(marker, goals, walls, rows, cols, grid_canvas, cell_size, find_multiple_paths)
        elif method == "CUS2":
            result = ida_star(marker, goals, walls, rows, cols, grid_canvas, cell_size, find_multiple_paths)
        else:
            output_text.insert(tk.END, f"Method '{method}' not supported.\n")
            output_text.config(state=tk.DISABLED)
            return
    
        # Display results and highlight the final path
        if result and (find_multiple_paths or goals[0] in result[0]):
            if method == "CUS1" or method == "CUS2":
                path, node_count, directions, visited, steps, iterations = result
            else:
                path, node_count, directions, visited, steps = result
    
            # Output for finding goals
            full_method_name = method_full_names.get(method, method)
            print(f"Search Strategy: {full_method_name}")
            if find_multiple_paths:
                print(f"Goals Found: {', '.join(map(str, goals))}")
            else:
                print(f"Goal Found: {goals[0]}")
            if method == "CUS1" or method == "CUS2":
                print(f"Number of Iterations: {iterations}")
            print(f"Number of Nodes Visited: {node_count}")
            print(f"Path to Goal(s): {', '.join(directions)}")

            output_text.insert(tk.END, f"Search Strategy: {full_method_name}\n")
            if find_multiple_paths:
                output_text.insert(tk.END, f"Goals Found: {', '.join(map(str, goals))}\n")
            else:
                output_text.insert(tk.END, f"Goal Found: {goals[0]}\n")
            if method == "CUS1" or method == "CUS2":
                output_text.insert(tk.END, f"Number of Iterations: {iterations}\n")
            output_text.insert(tk.END, f"Number of Nodes Visited: {node_count}\n")
            output_text.insert(tk.END, f"Path to Goal(s): {', '.join(directions)}\n")

            highlight_final_path(grid_canvas, path, goals, cell_size)  # Ensure path cells, including goals, are blue
            yellow_square = create_yellow_square(grid_canvas, marker[0], marker[1], cell_size)
            animate_path(grid_canvas, yellow_square, path, cell_size)
    
        else:
            output_text.insert(tk.END, "No path found.\n")
    
        output_text.config(state=tk.DISABLED)

    # Run the search function initially
    run_search()

    window.mainloop()