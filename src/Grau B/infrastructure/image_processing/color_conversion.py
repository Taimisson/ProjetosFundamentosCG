"""
Implementação de conversões de espaço de cor.
"""
import cv2 as cv
import numpy as np
from domain.entities.image import Image
from domain.interfaces.image_processor import ImageProcessorInterface


class GrayscaleProcessor(ImageProcessorInterface):
    """Converte imagem colorida para escala de cinza."""
    
    def __init__(self, method: str = 'weighted'):
        """
        Inicializa o processador de conversão para grayscale.
        
        Args:
            method: Método de conversão ('weighted', 'average', 'opencv')
                   - weighted: média ponderada (0.21R + 0.71G + 0.07B)
                   - average: média aritmética simples
                   - opencv: método padrão do OpenCV
        """
        self.method = method
    
    def process(self, image: Image) -> Image:
        """
        Converte imagem para escala de cinza.
        
        Args:
            image: Imagem de entrada (RGB)
            
        Returns:
            Imagem em grayscale
        """
        if image.channels == 1:
            # Já está em grayscale
            return image.copy()
        
        if self.method == 'opencv':
            # Método padrão do OpenCV
            gray = cv.cvtColor(image.data, cv.COLOR_BGR2GRAY)
        
        elif self.method == 'average':
            # Média aritmética dos canais
            gray = np.mean(image.data, axis=2).astype(np.uint8)
        
        else:  # weighted
            # Média ponderada (percepção do olho humano)
            b, g, r = cv.split(image.data)
            gray = (r * 0.21 + g * 0.71 + b * 0.07).astype(np.uint8)
        
        return Image(
            data=gray,
            width=image.width,
            height=image.height,
            channels=1,
            name=f"{image.name}_grayscale_{self.method}",
            path=None
        )


class HSVConverter(ImageProcessorInterface):
    """Converte imagem de RGB para HSV."""
    
    def process(self, image: Image) -> Image:
        """
        Converte imagem RGB para espaço de cor HSV.
        
        Args:
            image: Imagem de entrada (RGB)
            
        Returns:
            Imagem em HSV
        """
        hsv = cv.cvtColor(image.data, cv.COLOR_BGR2HSV)
        
        return Image(
            data=hsv,
            width=image.width,
            height=image.height,
            channels=3,
            name=f"{image.name}_hsv",
            path=None
        )


class ChannelSeparator(ImageProcessorInterface):
    """Separa canais individuais de uma imagem."""
    
    def __init__(self, channel: str = 'all'):
        """
        Inicializa o separador de canais.
        
        Args:
            channel: Canal a extrair ('r', 'g', 'b', 'h', 's', 'v', 'all')
        """
        self.channel = channel.lower()
    
    def process(self, image: Image) -> Image:
        """
        Extrai canal específico da imagem.
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Canal extraído como imagem grayscale
        """
        if image.channels == 1:
            return image.copy()
        
        # Mapeia canal para índice
        channel_map = {
            'b': 0, 'g': 1, 'r': 2,  # BGR
            'h': 0, 's': 1, 'v': 2   # HSV
        }
        
        if self.channel in channel_map:
            channel_data = image.data[:, :, channel_map[self.channel]]
            
            return Image(
                data=channel_data,
                width=image.width,
                height=image.height,
                channels=1,
                name=f"{image.name}_channel_{self.channel}",
                path=None
            )
        
        # Se 'all', retorna a imagem original
        return image.copy()


class ChannelVisualizer(ImageProcessorInterface):
    """Cria visualização colorida de um canal específico."""
    
    def __init__(self, channel: str = 'r'):
        """
        Inicializa o visualizador de canal.
        
        Args:
            channel: Canal a visualizar ('r', 'g', 'b')
        """
        self.channel = channel.lower()
    
    def process(self, image: Image) -> Image:
        """
        Cria visualização colorida de um canal.
        
        Args:
            image: Imagem de entrada (RGB)
            
        Returns:
            Imagem com apenas o canal selecionado ativo
        """
        if image.channels == 1:
            return image.copy()
        
        # Cria cópia da imagem
        result = np.zeros_like(image.data)
        
        # Ativa apenas o canal selecionado
        channel_map = {'b': 0, 'g': 1, 'r': 2}
        
        if self.channel in channel_map:
            idx = channel_map[self.channel]
            result[:, :, idx] = image.data[:, :, idx]
        
        return Image(
            data=result,
            width=image.width,
            height=image.height,
            channels=3,
            name=f"{image.name}_only_{self.channel}",
            path=None
        )
