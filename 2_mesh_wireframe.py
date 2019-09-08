from objreader import *
from minigl import *
import utils
from gui import MainWindow

import tkinter
from PIL import Image, ImageTk

width = 800
height = 800
padding = 10


def map_to_screen(v):
    return [(v[0] + 1) * (width - padding) / 2, (v[1] + 1) * (height - padding)/2, v[2]]


if __name__ == "__main__":
    image = utils.createImage(width, height)
    m = Model("obj/african_head.obj")

    for i, f in enumerate(m.faces):
        v = [map_to_screen(m.vertices[f[i][0]]) for i in range(3)]
        line(v[0], v[1], image, utils.WHITE)
        line(v[1], v[2], image, utils.WHITE)
        line(v[0], v[2], image, utils.WHITE)

    utils.saveImage("out/2_mesh_wireframe.jpg", image)

    window = MainWindow(width, height)
    window.showImage(image)