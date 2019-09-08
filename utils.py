import numpy as np
from skimage import io

RED = [1, 0, 0]
GREEN = [0, 1, 0]
BLUE = [0, 0, 1]
BLACK = [0, 0, 0]
WHITE = [1, 1, 1]


def RANDOM(): return np.random.randint(0, 255, (1, 3))


def createImage(width, height):
    return np.zeros((width, height, 3))


def saveImage(filename, image):
    image = np.transpose(image, axes=(1, 0, 2))
    image = np.flipud(image)
    if image.dtype == np.float64:
        image = (image * 255).astype(np.uint8)
    io.imsave(filename, image)
