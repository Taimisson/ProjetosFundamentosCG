"""
Implementação de filtros passa-alta (detecção de bordas).
"""
import cv2 as cv
import numpy as np
from domain.entities.image import Image
from domain.interfaces.image_processor import ImageProcessorInterface


class LaplacianFilterProcessor(ImageProcessorInterface):
    """Aplica filtro Laplaciano para detecção de bordas."""
    
    def __init__(self, kernel_size: int = 3):
        """
        Inicializa o processador de filtro Laplaciano.
        
        Args:
            kernel_size: Tamanho do kernel (1, 3, 5, ou 7)
        """
        self.kernel_size = kernel_size
    
    def process(self, image: Image) -> Image:
        """
        Aplica filtro Laplaciano na imagem.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem com bordas detectadas
        """
        # Converte para grayscale se necessário
        if image.channels == 3:
            gray = cv.cvtColor(image.data, cv.COLOR_BGR2GRAY)
        else:
            gray = image.data
        
        # Aplica o filtro Laplaciano
        laplacian = cv.Laplacian(gray, cv.CV_64F, ksize=self.kernel_size)
        
        # Converte de volta para uint8
        processed_data = cv.convertScaleAbs(laplacian)
        
        return Image(
            data=processed_data,
            width=image.width,
            height=image.height,
            channels=1,
            name=f"{image.name}_laplacian",
            path=None
        )


class SobelFilterProcessor(ImageProcessorInterface):
    """Aplica filtro Sobel para detecção de bordas."""
    
    def __init__(self, kernel_size: int = 3, direction: str = 'both'):
        """
        Inicializa o processador de filtro Sobel.
        
        Args:
            kernel_size: Tamanho do kernel (1, 3, 5, ou 7)
            direction: Direção do filtro ('x', 'y', ou 'both')
        """
        self.kernel_size = kernel_size
        self.direction = direction
    
    def process(self, image: Image) -> Image:
        """
        Aplica filtro Sobel na imagem.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem com bordas detectadas
        """
        # Converte para grayscale se necessário
        if image.channels == 3:
            gray = cv.cvtColor(image.data, cv.COLOR_BGR2GRAY)
        else:
            gray = image.data
        
        # Aplica o filtro Sobel
        if self.direction == 'x':
            sobel = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=self.kernel_size)
        elif self.direction == 'y':
            sobel = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=self.kernel_size)
        else:  # both
            sobel_x = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=self.kernel_size)
            sobel_y = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=self.kernel_size)
            sobel = cv.magnitude(sobel_x, sobel_y)
        
        # Converte de volta para uint8
        processed_data = cv.convertScaleAbs(sobel)
        
        return Image(
            data=processed_data,
            width=image.width,
            height=image.height,
            channels=1,
            name=f"{image.name}_sobel_{self.direction}",
            path=None
        )
