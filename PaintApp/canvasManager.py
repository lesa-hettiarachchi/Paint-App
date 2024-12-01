class CanvasManager:
    def __init__(self, canvas, app):
        self.canvas = canvas
        self.app = app
        self.eraserColor="white"
        self.penColor = "black"

        # Bind pen (default tool)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.resetPreviousPoint)
        self.canvas.bind("<ButtonPress-1>", self.startNewActionGroup)

    def startNewActionGroup(self, event):
        self.current_action_group = []

    # ----------------- Pen Drawing ------------------------
    def pen(self):
        self.app.stroke_color.set(self.penColor)
        self.canvas["cursor"] = "pencil"
        self.canvas.bind("<B1-Motion>", self.paint)

    def paint(self, event):
        x, y = event.x, event.y
        self.app.currentPoint = [x, y]

        if self.app.prevPoint != [0, 0]:

            line = self.canvas.create_line(
                self.app.prevPoint[0], self.app.prevPoint[1],
                x, y,
                fill=self.app.stroke_color.get(),
                width=self.app.stroke_size.get(),
                capstyle="round",
                smooth=True
            )

            self.current_action_group.append(line)


        self.app.prevPoint = [x, y]

    def resetPreviousPoint(self, event):

        self.app.prevPoint = [0, 0]

        if self.current_action_group:
            self.app.actions.append(self.current_action_group)
            self.current_action_group = []

    # ----------------- Eraser -------------------------
    def eraser(self):
        self.app.stroke_color.set(self.eraserColor)
        self.canvas["cursor"] = "dotbox"
        self.canvas.bind("<B1-Motion>", self.paint)

    # ----------------- Rectangle Drawing -------------------------
    def rectangle(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = None

    def drawRectangle(self, event):
        self.canvas["cursor"] = "cross"
        if self.app.stroke_color.get() == self.eraserColor:
            self.app.stroke_color.set(self.penColor)
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline=self.app.stroke_color.get(), width=self.app.stroke_size.get()
        )
        self.current_action_group.append(self.rect)

    # ----------------- Circle Drawing -------------------------
    def circle(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.oval = None

    def drawCircle(self, event):
        self.canvas["cursor"] = "cross"
        if self.app.stroke_color.get() == self.eraserColor:
            self.app.stroke_color.set(self.penColor)
        if self.oval:
            self.canvas.delete(self.oval)
        self.oval = self.canvas.create_oval(
            self.start_x, self.start_y, event.x, event.y,
            outline=self.app.stroke_color.get(), width=self.app.stroke_size.get()
        )
        self.current_action_group.append(self.oval)