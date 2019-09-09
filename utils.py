import numpy as np
from skimage import io

RED = np.array([1, 0, 0])
GREEN = np.array([0, 1, 0])
BLUE = np.array([0, 0, 1])
BLACK = np.array([0, 0, 0])
WHITE = np.array([1, 1, 1])


def RANDOM(): return np.random.randint(0, 255, (1, 3))


def createImage(width, height):
    return np.zeros((width, height, 3))


def saveImage(filename, image):
    if image.ndim == 3:
        image = np.transpose(image, axes=(1, 0, 2))
    else:
        image = np.transpose(image, axes=(1, 0))
    image = np.flipud(image)
    if image.dtype == np.float64:
        image = (image * 255).astype(np.uint8)
    io.imsave(filename, image)
