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


def scan_x(x1, x2, y, image, color):
    image[int(x1):int(x2+0.5), y] = color


def triangle_line_sweep(v, image, color):
    v = v[v[:, 1].argsort()]
    a = np.array(v[0], dtype=np.int32)
    b = np.array(v[1], dtype=np.int32)
    c = np.array(v[2], dtype=np.int32)
    total_height = max(c[1] - a[1], 1)
    seg_height = max(b[1] - a[1], 1)
    for y in range(a[1], b[1]+1):
        alpha = (y - a[1]) / total_height
        beta = (y - a[1]) / seg_height
        x1 = a[0] + (c[0] - a[0]) * alpha
        x2 = a[0] + (b[0] - a[0]) * beta
        if x1 > x2:
            x1, x2 = x2, x1
        scan_x(x1, x2, y, image, color)
    seg_height = max(c[1] - b[1], 1)
    for y in range(b[1], c[1]+1):
        alpha = (y - a[1]) / total_height
        beta = (y - b[1]) / seg_height
        x1 = a[0] + (c[0] - a[0]) * alpha
        x2 = b[0] + (c[0] - b[0]) * beta
        if x1 > x2:
            x1, x2 = x2, x1
        scan_x(x1, x2, y, image, color)


def barycentric(a, b, c, p):
    """
        https://en.wikipedia.org/wiki/Barycentric_coordinate_system
        ax - cx    bx - cx
        ay - cy    by - cy
    """
    v = np.array([a, b, c])
    T = (v[:-1, :2] - v[-1, :2]).T
    T_inv = np.linalg.inv(T)
    bc = np.dot(T_inv, (p[:2] - v[-1, :2]))
    bc[-1] = 1 - bc.sum()
    return bc


def triangle(vert, image, z_buffer=None, shader=None):
    """
    Triangle rasterization using barycentric coordinates
    """
    bbmin = vert[:, 0:2].min(axis=0)
    bbmax = vert[:, 0:2].max(axis=0)
    bbmin = bbmin.clip(0, [image.shape[0]-1, image.shape[1]-1])
    bbmax = bbmax.clip(0, [image.shape[0]-1, image.shape[1]-1])

    # precompute matrix for finding barycentric coordinates.
    T = (vert[:-1, :2] - vert[-1, :2]).T
    T_inv = np.linalg.inv(T)

    # Get the bounds
    bbmin = np.array(bbmin, dtype=np.uint32)
    bbmax = np.array(bbmax + 0.5, dtype=np.uint32) + 1

    # Create pixel index arrays in the bounding box
    x = range(bbmin[0], bbmax[0])
    y = range(bbmin[1], bbmax[1])

    u, v = np.meshgrid(x, y, sparse=False)
    uv = np.array([u, v])
    uv = uv.transpose(1, 2, 0)

    # Compute barycentric coordinates  for each pixel
    bcd = uv - vert[-1, :2]
    bc = np.tensordot(T_inv, bcd, axes=(1, 2)).transpose(1, 2, 0)

    # Mask for pxels with condition a, b >= 0 and (a+b<=1)
    # Here, a, b & c are barycentric coordinates.
    t = np.logical_and(np.all(np.greater_equal(
        bc[:, :], 0), axis=-1), np.less_equal(bc.sum(axis=-1), 1))
    t = t.transpose(1, 0)

    # Expand to contain third barycentric coordinate as (1 - bc1 - bc2)
    bcw = np.zeros((bc.shape[0], bc.shape[1], 3))
    # bcw = np.append(bc, np.expand_dims(1 - bc.sum(axis=-1), axis=2), axis=2)
    bcw[:, :, :2] = bc
    bcw[:, :, 2] = 1 - bc.sum(axis=-1)
    bcw = bcw.transpose(1, 0, 2)

    if z_buffer is not None:
        # Compute the pixel depth from barycentric coordinates
        bc_z = np.tensordot(vert[:, 2], bcw, axes=(0, 2))

        # Update the mask and z_buffer
        bb_z_buffer = z_buffer[bbmin[0]:bbmax[0], bbmin[1]: bbmax[1]]
        t_z = (bb_z_buffer < bc_z)
        t = np.logical_and(t, t_z)
        bb_z_buffer[:] = np.where(t, bc_z, bb_z_buffer)

    # Get sliced view into the bounding box and set the color based on mask.
    bb = image[bbmin[0]:bbmax[0], bbmin[1]: bbmax[1]]

    if shader is None:
        # Apply barycentric coordinates as color.
        bb[:] = np.where(t[:, :,  np.newaxis], np.array(
            bcw * 255, dtype=np.uint8), bb)
    else:
        sh = shader(bcw)
        bb[:] = np.where(t[:, :,  np.newaxis], sh, bb)


def projection(coeff):
    p = np.identity(4)
    p[3, 2] = -1/coeff
    return p


def viewport(x, y, w, h, depth):
    m = np.identity(4)
    m[0, 3] = x + w / 2.
    m[1, 3] = y + h / 2.
    m[2, 3] = depth / 2.

    m[0, 0] = w / 2.
    m[1, 1] = h / 2.
    m[2, 2] = depth / 2.
    return m
