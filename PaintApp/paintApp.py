from tkinter import Canvas, Frame, Label, IntVar, StringVar, SUNKEN, NW
from toolbar import Toolbar
from canvasManager import CanvasManager
from tkinter import filedialog, messagebox
from PIL import Image
import os

class PaintApp:
    def __init__(self, root):
        self.root = root

        # -------------- variables --------------------
        self.stroke_size = IntVar()
        self.stroke_size.set(1)

        self.stroke_color = StringVar()
        self.stroke_color.set("black")

        self.previousColor = StringVar()
        self.previousColor.set("white")

        self.prevPoint = [0, 0]

        self.actions = []
        self.undone_actions = []

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(self.root, bg="white")
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.canvasManager = CanvasManager(self.canvas, self)
        self.uiBuilder()
        self.createStatusBar()

        self.root.bind("<Configure>", self.onResize)

    def uiBuilder(self):
        toolBarFrame = Frame(self.root, height=100, width=1100)
        toolBarFrame.grid(row=0, column=0, sticky=NW)

        self.toolbar = Toolbar(toolBarFrame, self)

    def createStatusBar(self):
        self.statusBar = Label(self.root, text="Tool: Pen  |    Size: 1   |   Color: ", bd=1, relief=SUNKEN, anchor="w")
        self.statusBar.grid(row=2, column=0, sticky="we")

        self.colorCanvas = Canvas(self.statusBar, width=20, height=20, highlightthickness=0)
        self.colorCanvas.place(x=240, y=1)

    def updateStatusBar(self, tool, size, color):
        if tool == "Eraser":
            color = "white"

        self.statusBar.config(text=f"Tool: {tool}   |    Size: {size}   |   Color: ")

        self.colorCanvas.delete("color_rect")
        self.colorCanvas.create_rectangle(0, 0, 20, 20, fill=color, tags="color_rect")

    def undo(self):
        if self.actions:
            last_action_group = self.actions.pop()
            self.undone_actions.append(last_action_group)

            for item in last_action_group:
                self.canvas.itemconfigure(item, state='hidden')

    def redo(self):
        if self.undone_actions:
            action_group_to_redo = self.undone_actions.pop()
            self.actions.append(action_group_to_redo)

            for item in action_group_to_redo:
                self.canvas.itemconfigure(item, state='normal')

    def saveCanvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            try:
                ps_file = file_path.replace(".png", ".ps")
                self.canvas.postscript(file=ps_file)

                img = Image.open(ps_file)
                img.save(file_path, "png")


                os.remove(ps_file)

                messagebox.showinfo("Save", f"Canvas saved successfully at {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save the canvas: {str(e)}")

    def loadCanvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if file_path:
            try:
                from PIL import Image, ImageTk
                img = Image.open(file_path)
                self.loaded_image = ImageTk.PhotoImage(img)
                self.canvas.create_image(0, 0, image=self.loaded_image, anchor="nw")
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load the image: {str(e)}")

    def onResize(self, event):
        self.canvas.config(width=event.width, height=event.height - 100)

    def clear(self):
        should_clear = messagebox.askyesno("Clear Canvas", "Do you want to clear the entire canvas?")

        if should_clear:
            self.canvas.delete("all")