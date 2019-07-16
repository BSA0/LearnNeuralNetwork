import cv2 as cv
import numpy as np
import os

img = cv.imread("num20.bmp", 0)

dst = cv.resize(img, (104, 23))

cv.imwrite('num20.bmp', dst)

cv.destroyAllWindows()
