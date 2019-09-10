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

    start = np.array([0, 0])
    for i in range(1, 700):
        end = start + np.array([23, 5] if i % 2 else [5, 6])
        end = end % [width, height]
        side = (start + end) / 2
        side_dir = (start - end)[::-1] * [1, -1]
        side += side_dir
        side = side % [width, height]
        # line(start, end, image, utils.WHITE)
        i = i % 40
        triangle_line_sweep(np.array([start, end, side]), image, [
                            i*6, (40-i)*4, i*2])
        start = end

    utils.saveImage("out/3_triangle_strip.jpg", image)

    window = MainWindow(width, height)
    window.showImage(image)
