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
        self.entry_widgets = {}
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
                weight = math.sqrt((self.data['Coordinate_X'][i] - self.data['Coordinate_X'][elem - 1]) ** 2
                                   + (self.data['Coordinate_Y'][i] - self.data['Coordinate_Y'][elem - 1]) ** 2)
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

        self.buttons = {}  # Store buttons as a class attribute
        self.labels = {}   # Store labels as a class attribute
        self.entry_labels = {}  # Store labels for the entry rows as a class attribute

        # Add labels for "waga" and "ilość" rows on the left
        label_waga = tk.Label(root, text="Waga", anchor="e", padx=5)
        label_waga.place(relx=0.05, rely=0.9, anchor="center")

        label_ilosc = tk.Label(root, text="Ilość", anchor="e", padx=5)
        label_ilosc.place(relx=0.05, rely=0.95, anchor="center")

        label_waga = tk.Label(root, text="aktywacja \n kolor - aktywny \n zielony - p.konc\n niebieski p.start", anchor="e", padx=5)
        label_waga.place(relx=0.1, rely=0.75, anchor="center")

        # Add labels for "Ilość Kroków" and "Udźwig"
        label_liczba_krokow = tk.Label(root, text="Ilość Kroków", anchor="e", padx=5)
        label_liczba_krokow.place(relx=0.9, rely=0.6, anchor="center")

        label_udzwig = tk.Label(root, text="Udźwig wozka", anchor="e", padx=5)
        label_udzwig.place(relx=0.9, rely=0.7, anchor="center")

        for i, node in enumerate(nodes):
            button = tk.Button(root, text=str(node), command=lambda n=node: self.node_button_click(root, n))
            button.configure(bg='light gray')
            # Calculate x_tk for horizontal positioning
            x_tk = (i - (num_nodes - 1) / 2) * horizontal_spacing
            y_tk_buttons = 0.85  # Adjust the vertical position for buttons based on your preference

            button.place(relx=0.5 + x_tk, rely=y_tk_buttons, anchor="center")

            # Add an entry widget for each button in the first row
            entry_var_row1 = tk.IntVar()  # Variable to store the entry value for the first row
            entry_row1 = tk.Entry(root, textvariable=entry_var_row1, width=5)

            # Validate the entered value and set to 0 if not a positive integer
            entry_row1.place(relx=0.5 + x_tk, rely=y_tk_buttons + 0.05, anchor="center")
            self.entry_widgets[f"{node}_row1"] = entry_var_row1  # Store the entry variable for the first row

            # Add an entry widget for each button in the second row
            entry_var_row2 = tk.IntVar()  # Variable to store the entry value for the second row
            entry_row2 = tk.Entry(root, textvariable=entry_var_row2, width=5)
            entry_row2.place(relx=0.5 + x_tk, rely=y_tk_buttons + 0.1, anchor="center")
            self.entry_widgets[f"{node}_row2"] = entry_var_row2  # Store the entry variable for the second row

            self.buttons[node] = button

        # Add the first button (Zapisz)
        button1 = tk.Button(root, text="Zapisz", command=lambda: self.button1_click(root, self.entry_widgets, self.clicked_nodes))
        button1.place(relx=0.9, rely=0.25, anchor="center")

        # Add the second button (Button 2)
        button2 = tk.Button(root, text="Run", command=lambda: self.button2_click(root, self.entry_widgets))
        button2.place(relx=0.9, rely=0.35, anchor="center")

        # Add the third button (wyczyść)
        button3 = tk.Button(root, text="wyczyść", command=lambda: self.button3_click(root, self.entry_widgets))
        button3.place(relx=0.9, rely=0.45, anchor="center")
        self.clear_button = button3  # Store the clear button

        button4 = tk.Button(root, text=str(node), command=lambda n=node: self.node_button_click(root, n))
        button4.configure(bg='light gray')
            # Calculate x_tk for horizontal positioning

        # Add an entry widget for each button in the third row
        but3 = tk.IntVar()  # Variable to store the entry value for the fourth row
        entr_but3 = tk.Entry(root, textvariable=but3, width=5)
        entr_but3.place(relx=0.9, rely=0.75, anchor="center")
        self.entry_widgets[f"item_row3"] = but3  # # Store the entry variable for the third row

        # Add an entry widget for each item in the fourth row
        but4 = tk.IntVar()  # Variable to store the entry value for the fourth row
        entr_but4 = tk.Entry(root, textvariable=but4, width=5)
        entr_but4.place(relx=0.9, rely=0.65, anchor="center")
        self.entry_widgets[f"item_row4"] = but4  #



        root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root))  # Use a custom closing handler

        root.mainloop()




    def validate_entry(self, new_value, entry_var):
        try:
            # Spróbuj przekształcić wprowadzoną wartość na liczbę całkowitą
            value = int(new_value)

            # Jeśli wartość jest nieujemna, ustaw ją
            if value >= 0:
                entry_var.set(value)
            else:
                # Jeśli wartość jest ujemna, ustaw na 0
                entry_var.set(0)
        except ValueError:
            try:
                # Spróbuj przekształcić wprowadzoną wartość na liczbę z innego systemu liczbowego
                value = int(new_value, 0)
                
                # Jeśli wartość jest nieujemna, ustaw ją
                if value >= 0:
                    entry_var.set(value)
                else:
                    # Jeśli wartość jest ujemna, ustaw na 0
                    entry_var.set(0)
            except ValueError:
                # Jeśli wartość nie jest liczbą całkowitą, ustaw na 0
                entry_var.set(0)

    def node_button_click(self, root, node):
        button = self.get_button_by_text(root, str(node))

        # If the button is already clicked, unclick it and make it gray
        if node in self.clicked_buttons:
            
            self.unclick_all_buttons(root)
            button.configure(bg='light gray')
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

    def button1_click(self, root, entry_widgets, clicked_nodes):
        print("Button 1 Clicked")
        print("Clicked Nodes:", clicked_nodes)
        x = entry_widgets.get("item_row3").get()
        z = entry_widgets.get("item_row4").get()
        print(x, z)
        print(x,z)

        entry_values = {}
        for node in clicked_nodes:
            entry_var_row1 = entry_widgets.get(f"{node}_row1")
            entry_var_row2 = entry_widgets.get(f"{node}_row2")

            if entry_var_row1 and entry_var_row2:
                value_row1 = entry_var_row1.get()
                value_row2 = entry_var_row2.get()

                entry_values[node] = {'row1': value_row1, 'row2': value_row2}
                print(f"Values for Node {node} - Row 1: {value_row1}, Row 2: {value_row2}")

        if self.first_clicked_node:
            print("First Clicked Node:", self.first_clicked_node)
            print("Entry Values:", entry_values)

            # Calculate the sum of the values of the blue buttons in the same row as the green button
            sum_values_row1 = 0
            sum_values_row2 = 0
            for node in clicked_nodes[1:]:
                entry_var_row1 = entry_widgets.get(f"{node}_row1")
                entry_var_row2 = entry_widgets.get(f"{node}_row2")

                if entry_var_row1:
                    value_row1 = entry_var_row1.get()
                    sum_values_row1 += int(value_row1)

                if entry_var_row2:
                    value_row2 = entry_var_row2.get()
                    sum_values_row2 += int(value_row2)

            # Update the value of the green button in the same row with the calculated sum
            green_entry_var_row1 = entry_widgets.get(f"{self.first_clicked_node}_row1")
            green_entry_var_row2 = entry_widgets.get(f"{self.first_clicked_node}_row2")

            if green_entry_var_row1:
                green_entry_var_row1.set(sum_values_row1)

            if green_entry_var_row2:
                green_entry_var_row2.set(sum_values_row2)



    def button2_click(self, root, entry_widgets):
        print("Button 2 Clicked")
        way = [[5, 6], [6, 10], [10, 13], [13, 14], [1, 2]]
        self.open_new_window(way)  # Pass your desired 'way' parameter here

    def button3_click(self, root, entry_widgets):
        print("Button 3 Clicked")

        # Reset the color of all buttons to white
        for node, button in self.buttons.items():
            button.configure(bg='light gray')

            # Set the corresponding entry value to 0
            entry_var_row1 = entry_widgets.get(f"{node}_row1")
            entry_var_row2 = entry_widgets.get(f"{node}_row2")
            if entry_var_row1:
                entry_var_row1.set(0)
            if entry_var_row2:
                entry_var_row2.set(0)

        # Reset the color of the clear button to white
        if self.clear_button:
            self.clear_button.configure(bg='light gray')

        self.clicked_buttons.clear()
        self.clicked_nodes = []  # Clear the clicked nodes
        self.first_clicked_node = None

        # Unlock all columns

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
        for node, button in self.buttons.items():
            button.configure(bg='light gray')

            # Set the corresponding entry value to 0
            entry_var = self.entry_widgets.get(node)
            if entry_var:
                entry_var.set(0)

        self.clicked_buttons.clear()
        self.clicked_nodes = []  # Clear the clicked nodes
        self.first_clicked_node = None

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


