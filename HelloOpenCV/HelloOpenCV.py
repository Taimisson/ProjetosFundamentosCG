# Documentação oficial: https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html 

import numpy as np
import cv2 as cv

img = cv.imread('baboon.png')

cv.imshow('Hello',img)

k = cv.waitKey(0)