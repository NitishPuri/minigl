from minigl import *
import utils

image = utils.createImage(800, 800)

pixel((5, 5), image, (1, 1, 1))

aligned_rectangle((20, 20), (400, 40), image, (1, 1, 0))

line((20, 25), (60, 60), image, (1, 0, 1))
line((20, 25), (60, 100), image, (0, 1, 1))
line((20, 25), (100, 60), image, (0, 0, 1))
line((100, 25), (20, 60), image, (0, 0, 1))

utils.saveImage("out/1_primitives.jpg", image)


# Versions of line renderer.


def line_v1(a, b, image, color):
    # First attempt
    a = np.asarray(a)
    b = np.asarray(b)
    d = b - a
    for t in np.arange(0, 1.01, 0.01):
        p = (a + d*t).astype(int)
        pixel(p, image, color)


def line_v2(a, b, image, color):
    # Second  attempt
    a = np.asarray(a)
    b = np.asarray(b)
    d = b - a
    for x in np.arange(a[0], b[0]+1):
        t = (x - a[0])/(b[0] - a[0])
        y = int(a[1] * (1 - t) + b[1] * t)
        pixel((x, y), image, color)


def line_v3(a, b, image, color):
    # Third attempt
    a = np.asarray(a)
    b = np.asarray(b)
    d = b - a
    steep = False
    if(np.abs(d[0]) < np.abs(d[1])):
        a = a[::-1]
        b = b[::-1]
        d = b - a
        steep = True
    if a[0] > b[0]:
        a, b = b, a
    for x in np.arange(a[0], b[0]+1):
        t = (x - a[0])/(b[0] - a[0])
        y = int(a[1] * (1 - t) + b[1] * t)
        pixel((y, x) if steep else (x, y), image, color)
