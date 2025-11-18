"""
Implementação de operações de limiarização (thresholding).
"""
import cv2 as cv
import numpy as np
from domain.entities.image import Image
from domain.interfaces.image_processor import ImageProcessorInterface


class BinaryThresholdProcessor(ImageProcessorInterface):
    """Aplica limiarização binária."""
    
    def __init__(self, threshold: int = 127, max_value: int = 255):
        """
        Inicializa o processador de limiarização binária.
        
        Args:
            threshold: Valor de limiar (0-255)
            max_value: Valor máximo para pixels acima do limiar
        """
        self.threshold = threshold
        self.max_value = max_value
    
    def process(self, image: Image) -> Image:
        """
        Aplica limiarização binária na imagem.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem binarizada
        """
        # Converte para grayscale se necessário
        if image.channels == 3:
            gray = cv.cvtColor(image.data, cv.COLOR_BGR2GRAY)
        else:
            gray = image.data
        
        # Aplica limiarização binária
        _, binary = cv.threshold(gray, self.threshold, self.max_value, cv.THRESH_BINARY)
        
        return Image(
            data=binary,
            width=image.width,
            height=image.height,
            channels=1,
            name=f"{image.name}_binary_thresh_{self.threshold}",
            path=None
        )


class AdaptiveThresholdProcessor(ImageProcessorInterface):
    """Aplica limiarização adaptativa."""
    
    def __init__(self, block_size: int = 11, c: int = 2, method: str = 'gaussian'):
        """
        Inicializa o processador de limiarização adaptativa.
        
        Args:
            block_size: Tamanho da vizinhança (deve ser ímpar)
            c: Constante subtraída da média
            method: Método adaptativo ('mean' ou 'gaussian')
        """
        self.block_size = block_size if block_size % 2 == 1 else block_size + 1
        self.c = c
        self.method = method
    
    def process(self, image: Image) -> Image:
        """
        Aplica limiarização adaptativa na imagem.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem binarizada
        """
        # Converte para grayscale se necessário
        if image.channels == 3:
            gray = cv.cvtColor(image.data, cv.COLOR_BGR2GRAY)
        else:
            gray = image.data
        
        # Seleciona método adaptativo
        if self.method == 'mean':
            adaptive_method = cv.ADAPTIVE_THRESH_MEAN_C
        else:
            adaptive_method = cv.ADAPTIVE_THRESH_GAUSSIAN_C
        
        # Aplica limiarização adaptativa
        adaptive = cv.adaptiveThreshold(
            gray, 
            255, 
            adaptive_method, 
            cv.THRESH_BINARY, 
            self.block_size, 
            self.c
        )
        
        return Image(
            data=adaptive,
            width=image.width,
            height=image.height,
            channels=1,
            name=f"{image.name}_adaptive_{self.method}",
            path=None
        )


class OtsuThresholdProcessor(ImageProcessorInterface):
    """Aplica limiarização usando método de Otsu."""
    
    def process(self, image: Image) -> Image:
        """
        Aplica limiarização de Otsu na imagem.
        O método de Otsu calcula automaticamente o limiar ótimo.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem binarizada
        """
        # Converte para grayscale se necessário
        if image.channels == 3:
            gray = cv.cvtColor(image.data, cv.COLOR_BGR2GRAY)
        else:
            gray = image.data
        
        # Aplica limiarização de Otsu
        # O método calcula automaticamente o threshold ótimo
        threshold_value, otsu = cv.threshold(
            gray, 
            0, 
            255, 
            cv.THRESH_BINARY + cv.THRESH_OTSU
        )
        
        return Image(
            data=otsu,
            width=image.width,
            height=image.height,
            channels=1,
            name=f"{image.name}_otsu_thresh_{int(threshold_value)}",
            path=None
        )
