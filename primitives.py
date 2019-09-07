import numpy as np
from skimage import io

from minigl import *

image = np.zeros((250, 250, 3))
aligned_rectangle((20, 20), (40, 40), image, (1, 1, 0))
line((20, 25), (60, 60), image, (1, 0, 1))
line((20, 25), (60, 100), image, (0, 1, 1))
line((20, 25), (100, 60), image, (0, 0, 1))
line((100, 25), (20, 60), image, (0, 0, 1))
pixel((5, 5), image, (1, 1, 1))

saveImage("test2.jpg", image)
