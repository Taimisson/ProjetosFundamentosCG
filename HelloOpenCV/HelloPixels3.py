import numpy as np
import cv2 as cv

img = cv.imread('baboon.png')
imgResult = img.copy()
imgResult2 = img.copy()

altura = img.shape[0]
largura = img.shape[1]

#       B   G  R
cor = [0, 0, 255]

for i in range(altura):
    for j in range(largura):
        # Colorização
        imgResult[i,j,0] = imgResult[i,j,0] | cor[0]
        imgResult[i,j,1] = imgResult[i,j,1] | cor[1]
        imgResult[i,j,2] = imgResult[i,j,2] | cor[2]
        # Inversão
        imgResult2[i,j,0] = img[i,j,0] ^ 255
        imgResult2[i,j,1] = img[i,j,1] ^ 255
        imgResult2[i,j,2] = img[i,j,2] ^ 255

       
cv.imshow('Imagem Original', img)
cv.imshow('Imagem Colorizada', imgResult)
cv.imshow('Imagem Invertida', imgResult2)
cv.waitKey(0)