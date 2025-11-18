import numpy as np
import cv2 as cv

print(cv.__version__)

img = cv.imread('baboon.png')
imgResult = img.copy()
imgResult2 = img.copy()

altura = img.shape[0]
largura = img.shape[1]
nrCanais = img.shape[2]

for i in range(altura):
    for j in range(largura):
        b = img.item(i,j,0)
        g = img.item(i,j,1)
        r = img.item(i,j,2)

        # Conversão em grayscale usando média aritmética
        media = (r + g + b)/3.0
        imgResult[i, j, 0] = media
        imgResult[i, j, 1] = media
        imgResult[i, j, 2] = media

        # Conversão em grayscale usando média ponderada 
        # (percepção do olho humano)
        media = r * 0.21 + g * 0.71 + b * 0.07
        imgResult2[i, j, 0] = media
        imgResult2[i, j, 1] = media
        imgResult2[i, j, 2] = media



cv.imshow('Imagem Original', img)
cv.imshow('Imagem grayscale (média)',imgResult)
cv.imshow('Imagem grayscale (ponderada)',imgResult2)


cv.waitKey(0)