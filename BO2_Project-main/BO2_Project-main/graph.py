import matplotlib.image as mpimg
import networkx as nx
import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import os
import sys
from PIL import Image

class GraphApp:

    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        original_image_path = os.path.join(script_dir, 'data', 'logistics.jpg')

        # Specify the upscale factor (e.g., 2 for doubling the size)
        upscale_factor = 3
        # Load the original image using Pillow
        original_image = Image.open(original_image_path)

        # Upscale the image
        upscaled_image = original_image.resize((original_image.width * upscale_factor,
                                               original_image.height * upscale_factor))

        # Convert the upscaled image to a NumPy array
        self.image = mpimg.pil_to_array(upscaled_image)


        self.G = nx.Graph()
        self.data = pd.read_csv(os.path.join(script_dir, 'data', 'data.csv'))
        self.add_nodes()
        self.add_edges()

        self.clicked_buttons = set()
        self.clicked_nodes = []
        self.first_clicked_node = None

    def add_nodes(self):
        for i in range(16):
            self.G.add_node(i + 1, 
                            coordinates=(self.data['Coordinate_X'][i], self.data['Coordinate_Y'][i]),
                            label=self.data['City'][i])

    def add_edges(self):
        for i in range(16):
            connections = map(int, self.data['Connections'][i].split(';'))
            for elem in connections:
                weight = math.sqrt((self.data['Coordinate_X'][i] - self.data['Coordinate_X'][elem - 1])**2
                                   + (self.data['Coordinate_Y'][i] - self.data['Coordinate_Y'][elem - 1])**2)
                self.G.add_edge(i + 1, elem, weight=int(weight / 2.9724))

    def create_graph(self, way=None):
        fig, ax = plt.subplots()
        plt.imshow(self.image)

        pos = nx.get_node_attributes(self.G, 'coordinates')
        edge_labels = {(u, v): d['weight'] for u, v, d in self.G.edges(data=True)}

        nx.draw(self.G, pos=pos, with_labels=True, ax=ax, node_color='orange')  # Set node_color to 'orange'

        if way:
            nx.draw_networkx_edges(self.G, pos=pos, edgelist=way, width=3, edge_color='red', ax=ax)

        nx.draw_networkx_edge_labels(self.G, pos=pos, edge_labels=edge_labels, font_color='red', font_size=7, ax=ax)

        ax.axis('off')
        return fig

    def create_tkinter_window(self, root, fig):
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        nodes = sorted(self.G.nodes())  # Ensure the nodes are in order
        num_nodes = len(nodes)

        # Adjust the horizontal spacing between buttons
        horizontal_spacing = 0.05  # Adjust this value based on your preference

        for i, node in enumerate(nodes):
            button = tk.Button(root, text=str(node), command=lambda n=node: self.node_button_click(root, n))
            
            # Calculate x_tk for horizontal positioning
            x_tk = (i - (num_nodes - 1) / 2) * horizontal_spacing
            y_tk = 0.95  # Adjust the vertical position based on your preference
            
            button.place(relx=0.5 + x_tk, rely=y_tk, anchor="center")

        # Add the first button
        button1 = tk.Button(root, text="Zapisz", command=lambda: self.button1_click(root))
        button1.place(relx=0.9, rely=0.85, anchor="center")

        # Add the second button
        button2 = tk.Button(root, text="Button 2", command=lambda: self.button2_click(root))
        button2.place(relx=0.9, rely=0.75, anchor="center")

        # Add the second button
        button3 = tk.Button(root, text="wyczyść", command=lambda: self.button3_click(root))
        button3.place(relx=0.9, rely=0.65, anchor="center")

        root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root))  # Use a custom closing handler

        root.mainloop()

    def node_button_click(self, root, node):
        button = self.get_button_by_text(root, str(node))
        
        # If the button is already clicked, unclick it and make it gray
        if node in self.clicked_buttons:
            self.unclick_all_buttons(root)
            button.configure(bg='white')
            self.clicked_nodes = []  # Clear the clicked nodes
            self.first_clicked_node = None  # Reset the first clicked node
        else:
            # If two buttons are already clicked, unclick both and make them gray
            self.clicked_buttons.add(node)
            self.clicked_nodes.append(node)

            # Change button color based on the order of clicks
            if len(self.clicked_buttons) == 1:
                button.configure(bg='green')
                self.first_clicked_node = node  # Set the first clicked node
            elif len(self.clicked_buttons) > 1:
                button.configure(bg='blue')

    def button1_click(self, root):
        print("Button 1 Clicked")
        print("Clicked Nodes:", self.clicked_nodes)
        if self.first_clicked_node:
            print("First Clicked Node:", self.first_clicked_node)

    def button2_click(self, root):
        print("Button 2 Clicked")
        way = [[5, 6],[6, 10],[10, 13],[13, 14],[1,2]]
        self.open_new_window(way)  # Pass your desired 'way' parameter here

    def button3_click(self, root):
        print("Button 3 Clicked")
        self.unclick_all_buttons(root)
        self.clicked_nodes = []  # Clear the clicked nodes
        self.first_clicked_node = None 

        
    def on_closing(self, root):
        # Handle window closing
        print("Window closed")
        sys.exit()  # Exit the program

    def run(self, way=None):
        root = tk.Tk()
        root.title("NetworkX in Tkinter")

        graph_fig = self.create_graph(way)
        self.create_tkinter_window(root, graph_fig)

    def get_button_by_text(self, root, text):
        widgets = root.winfo_children()
        for widget in widgets:
            if isinstance(widget, tk.Button) and widget.cget("text") == text:
                return widget
        return None

    def unclick_all_buttons(self, root):
        for node in self.clicked_buttons:
            button = self.get_button_by_text(root, str(node))
            if button:
                button.configure(bg='white')
        self.clicked_buttons.clear()


    def create_graph_without_buttons(self, way=None):
            fig, ax = plt.subplots()
            plt.imshow(self.image)

            pos = nx.get_node_attributes(self.G, 'coordinates')
            edge_labels = {(u, v): d['weight'] for u, v, d in self.G.edges(data=True)}
            nx.draw(self.G, pos=pos, with_labels=True, ax=ax)

            if way:
                nx.draw_networkx_edges(self.G, pos=pos, edgelist=way, width=3, edge_color='red', ax=ax)

            nx.draw_networkx_edge_labels(self.G, pos=pos, edge_labels=edge_labels, font_color='red', font_size=7, ax=ax)

            ax.axis('off')
            return fig

    def open_new_window(self, way=None):
        root = tk.Tk()
        root.title("NetworkX in Tkinter")

        graph_fig = self.create_graph_without_buttons(way)
        canvas = FigureCanvasTkAgg(graph_fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root))  # Use a custom closing handler

        root.mainloop()

