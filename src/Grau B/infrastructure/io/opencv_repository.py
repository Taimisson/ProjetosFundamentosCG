"""
Implementação do repositório de imagens usando OpenCV.
"""
import cv2 as cv
import numpy as np
from pathlib import Path
from typing import Optional

from domain.entities.image import Image
from domain.interfaces.image_repository import ImageRepositoryInterface


class OpenCVImageRepository(ImageRepositoryInterface):
    """Repositório de imagens usando OpenCV para I/O."""
    
    def load(self, path: str) -> Image:
        """
        Carrega uma imagem usando OpenCV.
        
        Args:
            path: Caminho do arquivo de imagem
            
        Returns:
            Objeto Image com os dados carregados
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se a imagem não puder ser carregada
        """
        file_path = Path(path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Image file not found: {path}")
        
        # Carrega a imagem
        data = cv.imread(str(file_path))
        
        if data is None:
            raise ValueError(f"Failed to load image: {path}")
        
        # Extrai informações da imagem
        height, width = data.shape[:2]
        channels = data.shape[2] if len(data.shape) == 3 else 1
        
        return Image(
            data=data,
            width=width,
            height=height,
            channels=channels,
            name=file_path.stem,
            path=str(file_path)
        )
    
    def save(self, image: Image, path: str) -> bool:
        """
        Salva uma imagem usando OpenCV.
        
        Args:
            image: Objeto Image a ser salvo
            path: Caminho de destino
            
        Returns:
            True se salvo com sucesso, False caso contrário
        """
        try:
            # Garante que o diretório existe
            output_path = Path(path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Salva a imagem
            success = cv.imwrite(str(output_path), image.data)
            return success
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
