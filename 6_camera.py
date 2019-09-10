from objreader import *
from minigl import *
import utils
from gui import MainWindow
import time

width = 800
height = 800
depth = 255

eye = np.array([0, 0, 10], dtype=np.float)
center = np.array([0, 0, 0], dtype=np.float)
up = np.array([0, 1, 0], dtype=np.float)
# view_dir = (eye - center) * -1
# view_dir /= np.linalg.norm(view_dir)

Projection = projection(np.linalg.norm(eye - center))
# Projection = projection(1)
# Projection = np.identity(4)
Viewport = viewport(width/8, height/8,
                    width * 3/4, height * 3/4,
                    depth)
ModelView = lookat(eye, center, up)

ViewProjection = np.dot(np.dot(Viewport, Projection), ModelView)


def map_to_screen(v):
    v = np.dot(ViewProjection, np.append(v, 1))
    return v[:3] / v[3]


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
    utils.saveImage("out/6_camera.jpg", image)
    utils.saveImage("out/6_camera_zbuffer.jpg", z_buffer / depth)
    print(z_buffer.min(), z_buffer.max())
    timeend = time.perf_counter()
    print("Save to file :: ", (timeend - timestart), "s")

    window = MainWindow(width, height)
    window.showImage(image)
