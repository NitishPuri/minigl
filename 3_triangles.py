import tkinter
from objreader import *
from minigl import *
import utils

width = 800
height = 800

image = utils.createImage(width, height)

a = [10, 10]
b = [700, 50]
c = [300, 600]

triangle(a, b, c, image, utils.WHITE)

utils.saveImage("out/3_triangle.jpg", image)


def triangle_v1(a, b, c, image, color):
    line(a, b, image, color)
    line(b, c, image, color)
    line(c, a, image, color)
