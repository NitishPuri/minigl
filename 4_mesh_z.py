from objreader import *
from minigl import *
import utils
from gui import MainWindow
import time

width = 800
height = 800
depth = 600
padding = 10


def map_to_screen(v):
    return [(v[0] + 1) * (width - padding) / 2, (v[1] + 1) * (height - padding)/2, (v[2]+1) * depth / 2]


if __name__ == "__main__":
    timestart = time.perf_counter()
    image = utils.createImage(width, height)
    m = Model("obj/african_head.obj")
    timeend = time.perf_counter()
    print("Read model :: ", (timeend - timestart), "s")

    light_dir = np.array([0, 0, -1])

    timestart = time.perf_counter()
    z_buffer = np.zeros((width, height))
    for i, f in enumerate(m.faces):
        v = np.array([map_to_screen(m.vertices[f[i][0]]) for i in range(3)])

        normal = np.cross(v[2] - v[0], v[1] - v[0])
        normal /= np.linalg.norm(normal)
        intensity = abs(np.dot(normal, light_dir))

        # triangle_line_sweep(v, image, utils.WHITE * intensity)
        triangle(v, image, utils.WHITE * intensity, z_buffer)

    timeend = time.perf_counter()
    print("Render image :: ", (timeend - timestart), "s")

    timestart = time.perf_counter()
    utils.saveImage("out/4_mesh_light.jpg", image)
    utils.saveImage("out/4_mesh_light_zbuffer.jpg", z_buffer / depth)
    timeend = time.perf_counter()
    print("Save to file :: ", (timeend - timestart), "s")

    window = MainWindow(width, height)
    window.showImage(image)
