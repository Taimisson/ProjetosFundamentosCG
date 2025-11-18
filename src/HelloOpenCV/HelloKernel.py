import cv2 as cv
import numpy as np

img = cv.imread('baboon.png')

kernel = np.ones((9, 9), np.float32) / 81.0 

correlated_image = cv.filter2D(img, -1, kernel)

cv.imshow('Imagem original',img)
cv.imshow('Imagem transformada',correlated_image)

k = cv.waitKey(0)