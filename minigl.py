import numpy as np


def pixel(p, image, color):
    # During debugging only
    if p[0] < 0 or p[1] < 0 or p[0] >= image.shape[0] or p[1] >= image.shape[1]:
        print("ERROR :: Trying to paint pixel ", p)
        return
    image[int(p[0]), int(p[1])] = color


def aligned_rectangle(p, q, image, color):
    image[p[0]:q[0], p[1]:q[1]] = color


def line(a, b, image, color):
    a = np.asarray(a[:2])
    b = np.asarray(b[:2])
    d = b - a
    steep = False
    if(np.abs(d[0]) < np.abs(d[1])):
        a = a[::-1]
        b = b[::-1]
        steep = True
    if a[0] > b[0]:
        a, b = b, a
    d = b - a
    e = np.abs(d[1]/d[0])
    error = 0
    y = a[1]
    for x in np.arange(a[0], b[0]+1):
        pixel((y, x) if steep else (x, y), image, color)
        error += e
        if error > 0.5:
            y += 1 if b[1] > a[1] else -1
            error -= 1


def triangle(a, b, c, image, color):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    if a[1] > b[1]:
        a, b = b, a
    if a[1] > c[1]:
        a, c = c, a
    if b[1] > c[1]:
        a, c = c, a
    total_height = c[1] - a[1]
    seg_height = b[1] - a[1]
    for y in range(a[1], b[1]+1):
        alpha = (y - a[1]) / total_height
        beta = (y - a[1]) / seg_height
        A = a + (c - a) * alpha
        B = a + (b - a) * beta
        pixel(A, image, color)
        pixel(B, image, color)
    # seg_height = c[1] - b[1]
    # for y in range(b[1], c[1]):
    #     alpha = (y - a[1]) / total_height
    #     beta = (y - b[1]) / seg_height
    #     A = a + (c - a) * alpha
    #     B = a + (c - b) * beta
    #     pixel(A, image, utils.RED)
    #     pixel(B, image, utils.GREEN)
