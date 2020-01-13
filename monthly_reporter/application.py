"""
David Archuleta Jr.
"""
import tkinter as tk

from . import views as v

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("AFGJ Monthly Report Mover")
        self.geometry("400x200")
        self.resizable(width=False, height=False)

        self.main_frame = v.DirectoryFrame(self).grid(sticky=(tk.E + tk.W + tk.N + tk.S))
        self.columnconfigure(0, weight=1)