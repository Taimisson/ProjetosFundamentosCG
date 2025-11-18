# Documentação oficial: https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html 

import numpy as np
import cv2 as cv

img = cv.imread('baboon.png')

imgGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
imgBin = imgGray.copy()

b, g, r = cv.split(img)
rBin = r.copy()

altura = imgGray.shape[0]
largura = imgGray.shape[1]

k = int(input('Digite o limiar: '))

for i in range(altura):
    for j in range(largura):
        # Binarização da imagem Grayscale
        if (imgGray[i,j] < k):
            imgBin[i,j] = 0    
        else:
            imgBin[i,j] = 255
        # Binarização do canal vermelho
        if (r[i,j] < k):
            rBin[i,j] = 0
        else:
            rBin[i,j] = 255
   
cv.imshow('BGR (Original)',img)
cv.imshow('Grayscale',imgGray)
cv.imshow('Bin',imgBin)
cv.imshow('R',r)
cv.imshow('Bin R',rBin)

k = cv.waitKey(0)