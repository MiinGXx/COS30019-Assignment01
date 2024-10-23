def render_search_tree(parent_dict, canvas, node_radius=20, x_gap=60, y_gap=60):
    """
    Render the search tree dynamically on the canvas.
    Each node will be drawn in a tree structure with parent-child connections.
    """
    canvas.delete("all")  # Clear any previous drawing

    # Calculate the canvas dimensions
    canvas_width = canvas.winfo_width()

    # Dictionary to store the positions of each node (key=node, value=(x, y))
    node_positions = {}

    # Function to calculate the width of the subtree rooted at a given node
    def calculate_subtree_width(node):
        children = [child for child, parent in parent_dict.items() if parent == node]
        if not children:
            return 1  # Leaf nodes take up a width of 1 unit

        # Sum up the widths of all child subtrees
        subtree_width = 0
        for child in children:
            child_subtree_width = calculate_subtree_width(child)
            subtree_width += child_subtree_width

        return max(subtree_width, len(children))  # Ensure width is large enough for splitting

    # Recursive function to assign positions based on dynamically updated subtree width
    def assign_positions(node, depth, x_offset):
        # Calculate the width of the subtree rooted at this node
        subtree_width = calculate_subtree_width(node)

        # The x position is the middle of this subtree
        x = x_offset + (subtree_width / 2) * x_gap
        y = depth * y_gap
        node_positions[node] = (x, y)

        # Now, assign positions to the children
        children = [child for child, parent in parent_dict.items() if parent == node]
        if children:
            total_width = sum(calculate_subtree_width(child) for child in children)
            current_x_offset = x_offset

            # Adjust child positions evenly around the parent node
            for child in children:
                child_width = calculate_subtree_width(child)
                assign_positions(child, depth + 1, current_x_offset)
                current_x_offset += child_width * x_gap

    # Find the root (node with no parent)
    root = [node for node in parent_dict if parent_dict[node] is None][0]

    # Calculate the total width of the tree
    total_tree_width = calculate_subtree_width(root)

    # Assign positions to all nodes, starting from the root
    assign_positions(root, 0, 0)

    # Calculate the horizontal offset to center the tree on the canvas
    total_tree_pixel_width = total_tree_width * x_gap
    center_offset = (canvas_width - total_tree_pixel_width) // 2

    # Draw the edges (arrows) first, so they appear behind the nodes
    for node, (x, y) in node_positions.items():
        x += center_offset  # Apply centering offset to each node's x position
        if parent_dict[node] is not None:
            parent_x, parent_y = node_positions[parent_dict[node]]
            parent_x += center_offset
            canvas.create_line(parent_x, parent_y + node_radius, x, y - node_radius, fill="black", width=2)

    # Draw the nodes on top of the arrows
    for node, (x, y) in node_positions.items():
        x += center_offset  # Apply centering offset
        # Draw the node as a circle
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="lightblue", outline="black")
        canvas.create_text(x, y, text=str(node), font=("Arial", 10, "bold"))

    # Update the canvas display
    canvas.update()
