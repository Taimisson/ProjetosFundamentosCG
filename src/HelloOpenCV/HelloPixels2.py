import numpy as np
import cv2 as cv

img = cv.imread('baboon.png')

b, g, r = cv.split(img)

img2 = cv.merge([r,g,b])

cv.imshow('Imagem Original', img)
cv.imshow('Canal vermelho', r)
cv.imshow('Canal verde',g)
cv.imshow('Canal azul',b)
cv.imshow('Imagem unida',img2)

cv.waitKey(0)