"""
Interface para repositório de imagens.
"""
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.image import Image


class ImageRepositoryInterface(ABC):
    """Interface para operações de I/O de imagens."""
    
    @abstractmethod
    def load(self, path: str) -> Image:
        """
        Carrega uma imagem do sistema de arquivos.
        
        Args:
            path: Caminho do arquivo de imagem
            
        Returns:
            Objeto Image com os dados carregados
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o formato não for suportado
        """
        pass
    
    @abstractmethod
    def save(self, image: Image, path: str) -> bool:
        """
        Salva uma imagem no sistema de arquivos.
        
        Args:
            image: Objeto Image a ser salvo
            path: Caminho de destino
            
        Returns:
            True se salvo com sucesso, False caso contrário
        """
        pass
