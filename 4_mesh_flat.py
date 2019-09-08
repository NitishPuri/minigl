from objreader import *
from minigl import *
import utils
from gui import MainWindow
import time

width = 800
height = 800
padding = 10


def map_to_screen(v):
    return [(v[0] + 1) * (width - padding) / 2, (v[1] + 1) * (height - padding)/2, v[2]]


if __name__ == "__main__":
    timestart = time.perf_counter()
    image = utils.createImage(width, height)
    m = Model("obj/african_head.obj")
    timeend = time.perf_counter()
    print("Read model :: ", (timeend - timestart), "s")

    timestart = time.perf_counter()
    for i, f in enumerate(m.faces):
        v = np.array([map_to_screen(m.vertices[f[i][0]]) for i in range(3)])
        triangle_line_sweep(v, image, utils.WHITE)
        # triangle(v, image, utils.WHITE)
    timeend = time.perf_counter()
    print("Render image :: ", (timeend - timestart), "s")

    timestart = time.perf_counter()
    utils.saveImage("out/4_mesh_flat.jpg", image)
    timeend = time.perf_counter()
    print("Save to file :: ", (timeend - timestart), "s")

    window = MainWindow(width, height)
    window.showImage(image)
