"""
Implementação de filtros passa-baixa (suavização).
"""
import cv2 as cv
import numpy as np
from domain.entities.image import Image
from domain.interfaces.image_processor import ImageProcessorInterface


class MeanFilterProcessor(ImageProcessorInterface):
    """Aplica filtro de média para suavização."""
    
    def __init__(self, kernel_size: tuple = (3, 3)):
        """
        Inicializa o processador de filtro de média.
        
        Args:
            kernel_size: Tamanho do kernel (largura, altura)
        """
        self.kernel_size = kernel_size
    
    def process(self, image: Image) -> Image:
        """
        Aplica filtro de média na imagem.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem suavizada
        """
        # Cria kernel de média
        kernel = np.ones(self.kernel_size, np.float32) / (self.kernel_size[0] * self.kernel_size[1])
        
        # Aplica o filtro
        processed_data = cv.filter2D(image.data, -1, kernel)
        
        return Image(
            data=processed_data,
            width=image.width,
            height=image.height,
            channels=image.channels,
            name=f"{image.name}_mean_{self.kernel_size[0]}x{self.kernel_size[1]}",
            path=None
        )


class GaussianFilterProcessor(ImageProcessorInterface):
    """Aplica filtro Gaussiano para suavização."""
    
    def __init__(self, kernel_size: tuple = (5, 5), sigma: float = 1.0):
        """
        Inicializa o processador de filtro Gaussiano.
        
        Args:
            kernel_size: Tamanho do kernel (deve ser ímpar)
            sigma: Desvio padrão do Gaussiano
        """
        self.kernel_size = kernel_size
        self.sigma = sigma
    
    def process(self, image: Image) -> Image:
        """
        Aplica filtro Gaussiano na imagem.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem suavizada
        """
        processed_data = cv.GaussianBlur(image.data, self.kernel_size, self.sigma)
        
        return Image(
            data=processed_data,
            width=image.width,
            height=image.height,
            channels=image.channels,
            name=f"{image.name}_gaussian_{self.kernel_size[0]}x{self.kernel_size[1]}",
            path=None
        )
