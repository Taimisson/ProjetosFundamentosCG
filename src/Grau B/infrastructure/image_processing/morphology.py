"""
Implementação de transformações morfológicas.
"""
import cv2 as cv
import numpy as np
from domain.entities.image import Image
from domain.interfaces.image_processor import ImageProcessorInterface


class MorphologyProcessor(ImageProcessorInterface):
    """Classe base para operações morfológicas."""
    
    def __init__(self, kernel_size: tuple = (5, 5), kernel_shape: str = 'rect'):
        """
        Inicializa o processador morfológico.
        
        Args:
            kernel_size: Tamanho do elemento estruturante
            kernel_shape: Forma do elemento ('rect', 'ellipse', 'cross')
        """
        self.kernel_size = kernel_size
        self.kernel = self._create_kernel(kernel_shape)
    
    def _create_kernel(self, shape: str) -> np.ndarray:
        """Cria o elemento estruturante."""
        if shape == 'ellipse':
            return cv.getStructuringElement(cv.MORPH_ELLIPSE, self.kernel_size)
        elif shape == 'cross':
            return cv.getStructuringElement(cv.MORPH_CROSS, self.kernel_size)
        else:  # rect
            return cv.getStructuringElement(cv.MORPH_RECT, self.kernel_size)
    
    def process(self, image: Image) -> Image:
        """Método abstrato a ser implementado pelas subclasses."""
        raise NotImplementedError


class ErosionProcessor(MorphologyProcessor):
    """Aplica erosão morfológica."""
    
    def process(self, image: Image) -> Image:
        """Aplica erosão na imagem."""
        processed_data = cv.erode(image.data, self.kernel, iterations=1)
        
        return Image(
            data=processed_data,
            width=image.width,
            height=image.height,
            channels=image.channels,
            name=f"{image.name}_erosion",
            path=None
        )


class DilationProcessor(MorphologyProcessor):
    """Aplica dilatação morfológica."""
    
    def process(self, image: Image) -> Image:
        """Aplica dilatação na imagem."""
        processed_data = cv.dilate(image.data, self.kernel, iterations=1)
        
        return Image(
            data=processed_data,
            width=image.width,
            height=image.height,
            channels=image.channels,
            name=f"{image.name}_dilation",
            path=None
        )


class OpeningProcessor(MorphologyProcessor):
    """Aplica abertura morfológica (erosão seguida de dilatação)."""
    
    def process(self, image: Image) -> Image:
        """Aplica abertura na imagem."""
        processed_data = cv.morphologyEx(image.data, cv.MORPH_OPEN, self.kernel)
        
        return Image(
            data=processed_data,
            width=image.width,
            height=image.height,
            channels=image.channels,
            name=f"{image.name}_opening",
            path=None
        )


class ClosingProcessor(MorphologyProcessor):
    """Aplica fechamento morfológico (dilatação seguida de erosão)."""
    
    def process(self, image: Image) -> Image:
        """Aplica fechamento na imagem."""
        processed_data = cv.morphologyEx(image.data, cv.MORPH_CLOSE, self.kernel)
        
        return Image(
            data=processed_data,
            width=image.width,
            height=image.height,
            channels=image.channels,
            name=f"{image.name}_closing",
            path=None
        )


class GradientProcessor(MorphologyProcessor):
    """Aplica gradiente morfológico (diferença entre dilatação e erosão)."""
    
    def process(self, image: Image) -> Image:
        """Aplica gradiente morfológico na imagem."""
        processed_data = cv.morphologyEx(image.data, cv.MORPH_GRADIENT, self.kernel)
        
        return Image(
            data=processed_data,
            width=image.width,
            height=image.height,
            channels=image.channels,
            name=f"{image.name}_gradient",
            path=None
        )
