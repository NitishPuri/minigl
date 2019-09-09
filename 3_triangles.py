from objreader import *
from minigl import *
import utils
from gui import MainWindow

width = 600
height = 600


def triangle_v1(a, b, c, image, color):
    line(a, b, image, color)
    line(b, c, image, color)
    line(c, a, image, color)


if __name__ == "__main__":
    image = utils.createImage(width, height)

    a = [100, 100]
    b = [500, 50]
    c = [300, 500]

    v = np.array([a, b, c])

    triangle_line_sweep(v, image, utils.WHITE)

    triangle(v, image, utils.RED)

    utils.saveImage("out/3_triangle_2_2.jpg", image)

    window = MainWindow(width, height)
    window.showImage(image)
