import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import sys

# Your neighbor_matrix
neighbor_matrix = {
    0: {1: [10, 0], 2: [12, 0], 3: [11, 0], 4: [9, 0], 5: [8, 0]},
    1: {0: [10, 0], 2: [11, 20], 3: [15, 30], 4: [22, 25], 5: [12, 8]},
    2: {0: [12, 0], 1: [11, 20], 3: [7, 11], 4: [22, 35], 5: [12, 8]},
    3: {0: [11, 0], 1: [15, 30], 2: [7, 11], 4: [13, 20], 5: [35, 40]},
    4: {0: [9, 0], 1: [22, 35], 2: [23, 32], 3: [13, 20], 5: [16, 25]},
    5: {0: [8, 0], 1: [12, 8], 2: [15, 22], 3: [35, 40], 4: [16, 25]}
}

G = nx.DiGraph()

# Add edges to the graph with weights
for start_point, end_points in neighbor_matrix.items():
    for end_point, (time, steps) in end_points.items():
        G.add_edge(start_point, end_point, time=time, steps=steps)

# Create a layout for our nodes
pos = nx.spring_layout(G)

# Create Tkinter window
root = tk.Tk()
root.title("Graph Viewer")

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

# Create some example buttons
button1 = tk.Button(button_frame, text="Button 1", command=lambda: print("Button 1 clicked"))
button1.pack(side=tk.LEFT, padx=10)

button2 = tk.Button(button_frame, text="Button 2", command=lambda: print("Button 2 clicked"))
button2.pack(side=tk.LEFT, padx=10)

# Initialize the plot
fig, ax = plt.subplots()

# Draw the graph
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", arrowsize=15)

# Embed the matplotlib figure in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Start the Tkinter event loop
def on_closing():
    root.destroy()
    sys.exit()

# Set the window close event callback
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()