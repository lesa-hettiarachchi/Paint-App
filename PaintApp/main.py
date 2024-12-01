from tkinter import Tk
from paintApp import PaintApp

class MainApp:
    def __init__(self):
        root = Tk()
        root.title("Paint App")
        root.geometry("1100x600")
        PaintApp(root)
        root.mainloop()

if __name__ == "__main__":
    MainApp()
