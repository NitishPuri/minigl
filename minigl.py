import numpy as np


def pixel(p, image, color):
    image[int(p[0]), int(p[1])] = color


def aligned_rectangle(p, q, image, color):
    image[p[0]:q[0], p[1]:q[1]] = color

# First attempt


def line_v1(a, b, image, color):
    a = np.asarray(a)
    b = np.asarray(b)
    d = b - a
    for t in np.arange(0, 1.01, 0.01):
        p = (a + d*t).astype(int)
        pixel(p, image, color)

# Second  attempt


def line_v2(a, b, image, color):
    a = np.asarray(a)
    b = np.asarray(b)
    d = b - a
    for x in np.arange(a[0], b[0]+1):
        t = (x - a[0])/(b[0] - a[0])
        y = int(a[1] * (1 - t) + b[1] * t)
        pixel((x, y), image, color)

# Third attempt


def line_v3(a, b, image, color):
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

# Fourth attempt


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
