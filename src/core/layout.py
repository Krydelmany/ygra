"""
Layout calculation for B-tree visualization.
"""
from typing import List, Dict, Any, Tuple
from .btree import BTree, BNode


def layout(tree: BTree) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Calculate layout positions for all nodes and edges.

    Returns:
        (nodes, edges) where:
        - nodes: [{"id": str, "keys": List[int], "x": float, "y": float, "isLeaf": bool}]
        - edges: [{"fromId": str, "toId": str}]
    """
    if not tree.root:
        return [], []

    nodes = []
    edges = []

    # Calculate positions using level-order traversal with width calculation
    levels = _build_level_data(tree.root)
    _assign_positions(levels, nodes, edges)

    return nodes, edges


def _build_level_data(root: BNode) -> List[List[BNode]]:
    """Build level-by-level data for the tree."""
    levels = []
    queue = [root]

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.pop(0)
            current_level.append(node)

            # Add children to queue
            for child in node.children:
                queue.append(child)

        levels.append(current_level)

    return levels


def _assign_positions(levels: List[List[BNode]], 
                     nodes: List[Dict[str, Any]], 
                     edges: List[Dict[str, Any]]):
    """Assign x,y positions to nodes and create edge list."""
    LEVEL_HEIGHT = 120  # Vertical spacing between levels
    MIN_NODE_SPACING = 150  # Minimum horizontal spacing between nodes

    # Calculate subtree widths (number of leaves under each node)
    subtree_widths = _calculate_subtree_widths(levels)

    for level_idx, level in enumerate(levels):
        y = level_idx * LEVEL_HEIGHT + 50  # Start at y=50

        # Calculate total width needed for this level
        total_width = 0
        for node in level:
            width = max(subtree_widths[node.id] * MIN_NODE_SPACING, MIN_NODE_SPACING)
            total_width += width

        # Center the level
        start_x = -total_width / 2
        current_x = start_x

        for node in level:
            node_width = max(subtree_widths[node.id] * MIN_NODE_SPACING, MIN_NODE_SPACING)
            x = current_x + node_width / 2

            # Add node to result
            nodes.append({
                "id": node.id,
                "keys": node.keys.copy(),
                "x": x,
                "y": y,
                "isLeaf": node.leaf
            })

            current_x += node_width

    # Create edges
    _create_edges(levels, edges)


def _calculate_subtree_widths(levels: List[List[BNode]]) -> Dict[str, int]:
    """Calculate the width (number of leaves) under each node."""
    widths = {}

    # Process levels bottom-up
    for level in reversed(levels):
        for node in level:
            if node.leaf:
                widths[node.id] = 1
            else:
                # Sum of children widths
                total_width = sum(widths[child.id] for child in node.children)
                widths[node.id] = max(total_width, 1)

    return widths


def _create_edges(levels: List[List[BNode]], edges: List[Dict[str, Any]]):
    """Create parent-child edges."""
    for level in levels:
        for node in level:
            for child in node.children:
                edges.append({
                    "fromId": node.id,
                    "toId": child.id
                })


def get_node_bounds(nodes: List[Dict[str, Any]]) -> Dict[str, float]:
    """Get bounding box of all nodes."""
    if not nodes:
        return {"minX": 0, "maxX": 0, "minY": 0, "maxY": 0}

    xs = [node["x"] for node in nodes]
    ys = [node["y"] for node in nodes]

    return {
        "minX": min(xs) - 100,
        "maxX": max(xs) + 100,
        "minY": min(ys) - 50,
        "maxY": max(ys) + 100
    }
