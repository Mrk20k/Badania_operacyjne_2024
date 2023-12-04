
import graph as gp
import tkinter as tk
from tkinter import ttk




def main():
    

    app = gp.GraphApp()
    root = tk.Tk()
    root.title("NetworkX in Tkinter")
    app.create_tkinter_window(root, app.create_graph())
    root.mainloop()

    

    

if __name__ == "__main__":

    main()
   # App()

