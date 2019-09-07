import numpy as np
from skimage import io

RED = [1, 0, 0]
GREEN = [0, 1, 0]
BLUE = [0, 0, 1]
BLACK = [0, 0, 0]
WHITE = [1, 1, 1]


def saveImage(filename, image):
    image = np.transpose(image, axes=(1, 0, 2))
    image = np.flipud(image)
    if image.dtype == np.float64:
        image = (image * 255).astype(np.uint8)
    io.imsave("out/2_mesh_wireframe.jpg", image)