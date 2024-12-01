from tkinter import Frame, Button, Label, OptionMenu, colorchooser, SUNKEN

class Toolbar:
    def __init__(self, frame, app):
        self.frame = frame
        self.app = app
        self.color="black"
        self.size=1
        self.tool="Pen"

        self.toolsBox()
        self.sizeBox()
        self.colorBox()
        self.optionsBox()
        self.shapeDrawer()

    def toolsBox(self):
        toolsFrame = Frame(self.frame, height=100, width=100, relief=SUNKEN)
        toolsFrame.grid(row=0, column=0)

        penButton = Button(toolsFrame, text="Pen", width=10, command=self.selectPen)
        penButton.grid(row=0, column=0)

        eraserButton = Button(toolsFrame, text="Eraser", width=10, command=self.selectEraser)
        eraserButton.grid(row=1, column=0)

        toolsLabel = Label(toolsFrame, text="Tools", width=10)
        toolsLabel.grid(row=2, column=0)

    def selectPen(self):
        self.app.canvasManager.pen()
        self.tool="Pen"
        self.color=self.app.stroke_color.get()
        self.app.updateStatusBar(self.tool, self.size, self.color)

    def selectEraser(self):
        self.app.canvasManager.eraser()
        self.tool="Eraser"
        self.app.updateStatusBar(self.tool,self.size,self.color)

    def sizeBox(self):
        sizeFrame = Frame(self.frame, height=100, width=100, relief=SUNKEN)
        sizeFrame.grid(row=0, column=1)

        sizeLabel = Label(sizeFrame, text="Size", width=10)
        sizeLabel.grid(row=0, column=0)

        sizeOption = OptionMenu(sizeFrame, self.app.stroke_size, 1, 2, 3, 4, 5, 10, 25, 50, command=self.sizeSetter )
        sizeOption.grid(row=1, column=0)

    def colorBox(self):
        colorFrame = Frame(self.frame, height=100, width=100, relief=SUNKEN)
        colorFrame.grid(row=0, column=2)

        colorButton = Button(colorFrame, text="Select Color", width=10, command=self.colorSelector)
        colorButton.grid(row=1, column=0)

    def shapeDrawer(self):
        shapesFrame = Frame(self.frame, height=100, width=100, relief=SUNKEN)
        shapesFrame.grid(row=0, column=3)

        rectButton = Button(shapesFrame, text="Rectangle", width=10, command=self.bindRectangle)
        rectButton.grid(row=0, column=0)

        circleButton = Button(shapesFrame, text="Circle", width=10, command=self.bindCircle)
        circleButton.grid(row=1, column=0)

        shapeLabel = Label(shapesFrame, text="Shapes", width=10)
        shapeLabel.grid(row=2, column=0)

    def optionsBox(self):
        optionsFrame = Frame(self.frame, height=100, width=300, relief=SUNKEN)
        optionsFrame.grid(row=0, column=6)

        undoButton = Button(optionsFrame, text="Undo", width=10, command=self.app.undo)
        undoButton.grid(row=1, column=0)

        redoButton = Button(optionsFrame, text="Redo", width=10, command=self.app.redo)
        redoButton.grid(row=2, column=0)

        clearButton = Button(optionsFrame, text="Clear", width=10, command=self.app.clear)
        clearButton.grid(row=1,column=1)

        saveButton = Button(optionsFrame, text="Save", width=10, command=self.app.saveCanvas)
        saveButton.grid(row=1, column=2)

        loadButton = Button(optionsFrame, text="Load", width=10, command=self.app.loadCanvas)
        loadButton.grid(row=2, column=2)

        optionsLabel = Label(optionsFrame, text="Options", width=10)
        optionsLabel.grid(row=3, column=1)

    def sizeSetter(self, selected_size):
        self.size = selected_size
        self.app.stroke_size.set(self.size)
        self.app.updateStatusBar(self.tool, self.size, self.color)

    def colorSelector(self):
        self.app.canvasManager.penColor = colorchooser.askcolor("blue", title="Select Color")[1]
        if self.app.canvasManager.penColor is None:
            self.app.stroke_color.set("black")
        else:
            self.app.stroke_color.set(self.app.canvasManager.penColor)
        self.color = self.app.stroke_color.get()
        self.app.updateStatusBar(self.tool, self.size, self.color)

    def bindRectangle(self):
        self.app.canvas["cursor"] = "cross"
        self.app.canvas.bind("<ButtonPress-1>", self.app.canvasManager.rectangle)
        self.app.canvas.bind("<B1-Motion>", self.app.canvasManager.drawRectangle)
        self.app.canvas.bind("<ButtonRelease-1>", self.app.canvasManager.resetPreviousPoint)
        self.tool="Rectangle"
        self.app.updateStatusBar(self.tool, self.size, self.color)

    def bindCircle(self):
        self.app.canvas["cursor"] = "cross"
        self.app.canvas.bind("<ButtonPress-1>", self.app.canvasManager.circle)
        self.app.canvas.bind("<B1-Motion>", self.app.canvasManager.drawCircle)
        self.app.canvas.bind("<ButtonRelease-1>", self.app.canvasManager.resetPreviousPoint)
        self.tool="Circle"
        self.app.updateStatusBar(self.tool, self.size, self.color)