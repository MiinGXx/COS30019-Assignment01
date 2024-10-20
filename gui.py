import tkinter as tk
from grid import create_grid, create_yellow_square, animate_path
from searchstrategy import dfs, bfs, gbfs, a_star, highlight_final_path, render_search_tree

def create_grid_window(rows, cols, marker, goals, walls, method, cell_size=50):
    window = tk.Tk()
    window.title("Grid Visualization")
    
    canvas = tk.Canvas(window, width=cols * cell_size, height=rows * cell_size)
    canvas.pack()
    
    create_grid(canvas, rows, cols, markers=[marker], goals=goals, walls=walls)
    
    if method == "DFS":
        path, node_count, directions, parent = dfs(marker, goals, walls, rows, cols, canvas, cell_size)
    elif method == "BFS":
        path, node_count, directions, parent = bfs(marker, goals, walls, rows, cols, canvas, cell_size)
    elif method == "GBFS":
        path, node_count, directions, parent = gbfs(marker, goals, walls, rows, cols, canvas, cell_size)
    elif method == "AS":
        path, node_count, directions, parent = a_star(marker, goals, walls, rows, cols, canvas, cell_size)
    else:
        print(f"Method '{method}' not supported.")
        return

    if path:
        highlight_final_path(canvas, path, cell_size)
        yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)
        animate_path(canvas, yellow_square, path)

        # Render the search tree
        render_search_tree(parent)  # Render the tree based on the parent dict

        print(f"{method} method")
        print(f"<Node {path[-1]}> {node_count}")
        print(f"[{' , '.join(directions)}]")
    else:
        print("No path to the goal was found.")

    window.mainloop()


