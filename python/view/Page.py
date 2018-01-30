import Tkinter as Tk


class Page(Tk.Frame):
    def __init__(self, *args, **kwargs):
        Tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()
