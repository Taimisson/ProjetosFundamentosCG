"""
Implementação de operações com histogramas.
"""
import cv2 as cv
import numpy as np
from domain.entities.image import Image
from domain.interfaces.image_processor import ImageProcessorInterface


class HistogramEqualizer(ImageProcessorInterface):
    """Aplica equalização de histograma."""
    
    def __init__(self, color_equalization: str = 'value'):
        """
        Inicializa o equalizador de histograma.
        
        Args:
            color_equalization: Como equalizar imagens coloridas
                               - 'value': equaliza apenas o canal V (HSV)
                               - 'all': equaliza todos os canais BGR
                               - 'grayscale': converte para gray e equaliza
        """
        self.color_equalization = color_equalization
    
    def process(self, image: Image) -> Image:
        """
        Equaliza o histograma da imagem.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem com histograma equalizado
        """
        if image.channels == 1:
            # Imagem grayscale
            equalized = cv.equalizeHist(image.data)
            channels = 1
        
        elif self.color_equalization == 'grayscale':
            # Converte para grayscale e equaliza
            gray = cv.cvtColor(image.data, cv.COLOR_BGR2GRAY)
            equalized = cv.equalizeHist(gray)
            channels = 1
        
        elif self.color_equalization == 'value':
            # Equaliza apenas o canal V (brilho) em HSV
            hsv = cv.cvtColor(image.data, cv.COLOR_BGR2HSV)
            hsv[:, :, 2] = cv.equalizeHist(hsv[:, :, 2])
            equalized = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
            channels = 3
        
        else:  # 'all'
            # Equaliza todos os canais BGR separadamente
            b, g, r = cv.split(image.data)
            b_eq = cv.equalizeHist(b)
            g_eq = cv.equalizeHist(g)
            r_eq = cv.equalizeHist(r)
            equalized = cv.merge([b_eq, g_eq, r_eq])
            channels = 3
        
        return Image(
            data=equalized,
            width=image.width,
            height=image.height,
            channels=channels,
            name=f"{image.name}_equalized_{self.color_equalization}",
            path=None
        )


class HistogramCalculator:
    """Calcula histograma de uma imagem."""
    
    @staticmethod
    def calculate(image: Image) -> dict:
        """
        Calcula histograma da imagem.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Dicionário com histogramas por canal
        """
        histograms = {}
        
        if image.channels == 1:
            # Histograma grayscale
            hist = cv.calcHist([image.data], [0], None, [256], [0, 256])
            histograms['gray'] = hist.flatten()
        
        else:
            # Histogramas RGB
            colors = ['b', 'g', 'r']
            for i, color in enumerate(colors):
                hist = cv.calcHist([image.data], [i], None, [256], [0, 256])
                histograms[color] = hist.flatten()
        
        return histograms


class CLAHEProcessor(ImageProcessorInterface):
    """Aplica CLAHE (Contrast Limited Adaptive Histogram Equalization)."""
    
    def __init__(self, clip_limit: float = 2.0, tile_grid_size: tuple = (8, 8)):
        """
        Inicializa o processador CLAHE.
        
        Args:
            clip_limit: Limite de contraste
            tile_grid_size: Tamanho da grade de tiles
        """
        self.clip_limit = clip_limit
        self.tile_grid_size = tile_grid_size
    
    def process(self, image: Image) -> Image:
        """
        Aplica CLAHE na imagem.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem com CLAHE aplicado
        """
        # Cria objeto CLAHE
        clahe = cv.createCLAHE(
            clipLimit=self.clip_limit, 
            tileGridSize=self.tile_grid_size
        )
        
        if image.channels == 1:
            # Imagem grayscale
            result = clahe.apply(image.data)
            channels = 1
        
        else:
            # Imagem colorida - aplica no canal V (HSV)
            hsv = cv.cvtColor(image.data, cv.COLOR_BGR2HSV)
            hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
            result = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
            channels = 3
        
        return Image(
            data=result,
            width=image.width,
            height=image.height,
            channels=channels,
            name=f"{image.name}_clahe",
            path=None
        )
