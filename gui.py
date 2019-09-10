import tkinter
import numpy as np
from PIL import Image, ImageTk
import numpy
import time


class MainWindow:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = tkinter.Tk()
        self.frame = tkinter.Frame(self.root, width=width, height=height)
        self.frame.pack()
        self.canvas = tkinter.Canvas(
            self.frame, bg="black", width=width, height=height)
        self.canvas.place(x=-2, y=-2)

        self.root.bind('<Escape>', lambda e: self.root.destroy())

        # self.root.after(0, self.start)  # INCREASE THE 0 TO SLOW IT DOWN
        # self.root.mainloop()

    def showImage(self, image):
        image = np.transpose(image, axes=(1, 0, 2))
        image = np.flipud(image)
        if image.dtype == np.float64:
            image = (image * 255).astype(np.uint8)

        im = Image.frombytes('RGB', (image.shape[1],
                                     image.shape[0]), image.astype('b').tostring())

        photo = ImageTk.PhotoImage(image=im)
        self.canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
        # self.canvas.pack()
        self.root.mainloop()
