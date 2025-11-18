"""
Interface para processadores de imagem.
"""
from abc import ABC, abstractmethod
from domain.entities.image import Image


class ImageProcessorInterface(ABC):
    """Interface base para processadores de imagem."""
    
    @abstractmethod
    def process(self, image: Image) -> Image:
        """
        Processa uma imagem aplicando uma transformação.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem processada
        """
        pass
