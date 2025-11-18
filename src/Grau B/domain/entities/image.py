"""
Entidade que representa uma imagem no domínio da aplicação.
"""
from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class Image:
    """
    Representa uma imagem com seus metadados.
    
    Attributes:
        data: Array numpy contendo os dados da imagem
        width: Largura da imagem em pixels
        height: Altura da imagem em pixels
        channels: Número de canais (1 para grayscale, 3 para RGB)
        name: Nome ou identificador da imagem
        path: Caminho do arquivo original (opcional)
    """
    data: np.ndarray
    width: int
    height: int
    channels: int
    name: str
    path: Optional[str] = None
    
    def __post_init__(self):
        """Valida os dados da imagem após inicialização."""
        if self.data is None or self.data.size == 0:
            raise ValueError("Image data cannot be empty")
        
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be positive")
        
        if self.channels not in [1, 3, 4]:
            raise ValueError("Channels must be 1 (grayscale), 3 (RGB), or 4 (RGBA)")
    
    def is_grayscale(self) -> bool:
        """Retorna True se a imagem é em escala de cinza."""
        return self.channels == 1
    
    def is_color(self) -> bool:
        """Retorna True se a imagem é colorida."""
        return self.channels >= 3
    
    def copy(self) -> 'Image':
        """Cria uma cópia profunda da imagem."""
        return Image(
            data=self.data.copy(),
            width=self.width,
            height=self.height,
            channels=self.channels,
            name=f"{self.name}_copy",
            path=self.path
        )
