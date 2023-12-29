


import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Your neighbor_matrix
neighbor_matrix = {
    0: {1: [10, 0], 2: [12, 0], 3: [11, 0], 4: [9, 0], 5: [8, 0]},
    1: {0: [10, 0], 2: [11, 20], 3: [15, 30], 4: [22, 25], 5: [12, 8]},
    2: {0: [12, 0], 1: [11, 20], 3: [7, 11], 4: [22, 35], 5: [12, 8]},
    3: {0: [11, 0], 1: [15, 30], 2: [7, 11], 4: [13, 20], 5: [35, 40]},
    4: {0: [9, 0], 1: [22, 35], 2: [23, 32], 3: [13, 20], 5: [16, 25]},
    5: {0: [8, 0], 1: [12, 8], 2: [15, 22], 3: [35, 40], 4: [16, 25]}
}

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph with weights
for start_point, end_points in neighbor_matrix.items():
    for end_point, (time, steps) in end_points.items():
        G.add_edge(start_point, end_point, time=time, steps=steps)

# Create a layout for our nodes 
pos = nx.spring_layout(G)

# Initialize the plot
fig, ax = plt.subplots()



# Draw the graph
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", arrowsize=15)

# Specify the order in which nodes are visited
visit_order = [0, 1, 2, 3, 4, 5, 0]

# Keep track of visited nodes
visited_nodes = set()

# Function to update the animation at each frame
def update(frame):
    ax.clear()
    nx.draw(G, pos, with_labels=True, node_size=700, font_size=8,node_color="skyblue", font_color="black", font_weight="bold", arrowsize=15)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): f"{d['time']}" for i, j, d in G.edges(data=True)})
    
    # Identify the currently visited node
    current_node = visit_order[frame % len(visit_order)]
    visited_nodes.add(current_node)
    
    # Highlight the currently visited node in blue
    nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_size=700, node_color="blue")
    
    # Reset color for previously visited nodes
    nx.draw_networkx_nodes(G, pos, nodelist=list(visited_nodes - {current_node}), node_size=700, node_color="skyblue")
    labels = {(i, j): f"T: {G[i][j]['time']}, S: {G[i][j]['steps']}" for i, j in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
  
    ax.set_title(f"Ruch: {frame}")

# Animate the movement between nodes
animation = FuncAnimation(fig, update, frames=sum(neighbor_matrix[node][successor][0] for node in visit_order for successor in G.successors(node)), interval=1000, repeat=False)

# Show the animation
plt.show()
