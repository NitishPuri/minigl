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
    image = utils.createImage(width, height, 3, np.uint8)
    m = Model("obj/african_head.obj")

    texture = utils.readImage("obj/african_head_diffuse.tga")
    texture = np.flipud(texture)
    texture = texture.transpose(1, 0, 2)
    print("texture.shape = {}, dtype = {}".format(texture.shape, texture.dtype))

    timeend = time.perf_counter()
    print("Read model :: ", (timeend - timestart), "s")

    light_dir = np.array([0, 0, -1])

    timestart = time.perf_counter()
    z_buffer = np.zeros((width, height))
    for f in m.faces:
        v = np.array([map_to_screen(m.vertices[f[i][0]]) for i in range(3)])
        t = np.array([m.tex[f[i][1]] for i in range(3)]).T

        # texture mapping
        def shader(bc):
            tc = np.tensordot(t, bc, axes=(1, 2))
            tc = tc.transpose(1, 2, 0) * np.array(texture.shape[:2])
            tc = np.clip(tc.astype(np.uint32), [0, 0], [
                         texture.shape[0]-1,  texture.shape[1]-1])
            tc = tc.transpose(2, 0, 1)
            return texture[tc.tolist()]

        triangle(v, image, z_buffer, shader)

    timeend = time.perf_counter()
    print("Render image :: ", (timeend - timestart), "s")

    timestart = time.perf_counter()
    utils.saveImage("out/5_mesh_tex.jpg", image)
    utils.saveImage("out/5_mesh_tex_zbuffer.jpg", z_buffer / depth)
    timeend = time.perf_counter()
    print("Save to file :: ", (timeend - timestart), "s")

    window = MainWindow(width, height)
    window.showImage(image)
