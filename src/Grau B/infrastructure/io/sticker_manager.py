"""
Gerenciador de stickers para imagens.

Permite sobrepor imagens PNG com canal alfa sobre frames.
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path


class Sticker:
    """Representa um sticker posicionado."""
    
    def __init__(self, image: np.ndarray, x: int, y: int):
        """
        Inicializa sticker.
        
        Args:
            image: Imagem do sticker (com canal alfa se possível)
            x: Posição X
            y: Posição Y
        """
        self.image = image
        self.x = x
        self.y = y
        

class StickerManager:
    """
    Gerencia sobreposição de stickers em imagens.
    """
    
    def __init__(self):
        """Inicializa gerenciador de stickers."""
        self.stickers: List[Sticker] = []
        self.available_stickers: dict = {}
        
    def load_sticker(self, name: str, path: str) -> bool:
        """
        Carrega sticker do disco.
        
        Suporta formatos: PNG (melhor - com transparência), JPG, GIF (sem animação)
        Redimensiona automaticamente stickers grandes para 150x150 pixels.
        
        Args:
            name: Nome identificador do sticker
            path: Caminho do arquivo de imagem
            
        Returns:
            True se carregou com sucesso
        """
        path_obj = Path(path)
        
        if not path_obj.exists():
            print(f"⚠️ Sticker não encontrado: {path}")
            return False
        
        # Verifica extensão
        ext = path_obj.suffix.lower()
        supported_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        
        if ext not in supported_formats:
            print(f"⚠️ Formato não suportado: {ext}")
            print(f"   Formatos aceitos: {', '.join(supported_formats)}")
            return False
            
        # Carrega com canal alfa (RGBA) se disponível
        sticker_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        
        if sticker_img is None:
            print(f"❌ Erro ao carregar sticker: {path}")
            return False
        
        # Redimensiona stickers grandes (limite: 150x150)
        max_dimension = 150
        height, width = sticker_img.shape[:2]
        
        if height > max_dimension or width > max_dimension:
            # Calcula novo tamanho mantendo proporção
            scale = max_dimension / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            # Redimensiona mantendo o canal alfa se presente
            sticker_img = cv2.resize(
                sticker_img, 
                (new_width, new_height), 
                interpolation=cv2.INTER_AREA
            )
            print(f"   📐 Redimensionado de {width}x{height} para {new_width}x{new_height}")
        
        # Aviso para formatos sem transparência
        if ext in ['.jpg', '.jpeg', '.gif']:
            print(f"ℹ️  {path_obj.name}: Formato sem transparência (use PNG para melhor resultado)")
            # Converte para RGBA adicionando canal alfa opaco
            if len(sticker_img.shape) == 2:
                # Grayscale -> RGBA
                sticker_img = cv2.cvtColor(sticker_img, cv2.COLOR_GRAY2BGRA)
            elif sticker_img.shape[2] == 3:
                # BGR -> BGRA (adiciona canal alfa 100% opaco)
                sticker_img = cv2.cvtColor(sticker_img, cv2.COLOR_BGR2BGRA)
        
        self.available_stickers[name] = sticker_img
        return True
    
    def add_sticker(self, name: str, x: int, y: int):
        """
        Adiciona sticker na posição especificada.
        
        Args:
            name: Nome do sticker previamente carregado
            x: Posição X
            y: Posição Y
        """
        if name not in self.available_stickers:
            print(f"⚠️ Sticker '{name}' não está carregado.")
            return
            
        sticker_img = self.available_stickers[name]
        self.stickers.append(Sticker(sticker_img, x, y))
        
    def clear_stickers(self):
        """Remove todos os stickers aplicados."""
        self.stickers.clear()
        
    def apply_stickers(self, frame: np.ndarray) -> np.ndarray:
        """
        Aplica todos os stickers no frame.
        
        Args:
            frame: Frame base
            
        Returns:
            Frame com stickers aplicados
        """
        result = frame.copy()
        
        for sticker in self.stickers:
            result = self._overlay_sticker(
                result, 
                sticker.image, 
                sticker.x, 
                sticker.y
            )
            
        return result
    
    def _overlay_sticker(
        self, 
        background: np.ndarray, 
        sticker: np.ndarray, 
        x: int, 
        y: int
    ) -> np.ndarray:
        """
        Sobrepõe sticker no background considerando canal alfa.
        
        Args:
            background: Imagem de fundo
            sticker: Imagem do sticker
            x: Posição X
            y: Posição Y
            
        Returns:
            Imagem com sticker aplicado
        """
        sticker_height, sticker_width = sticker.shape[:2]
        
        # Limites da área do sticker
        y1, y2 = y, y + sticker_height
        x1, x2 = x, x + sticker_width
        
        # Verifica se sticker cabe na imagem
        if y2 > background.shape[0] or x2 > background.shape[1]:
            return background
        if y1 < 0 or x1 < 0:
            return background
            
        # Sticker com canal alfa (RGBA)
        if sticker.shape[2] == 4:
            # Canal alfa normalizado
            alpha = sticker[:, :, 3] / 255.0
            bg_alpha = 1.0 - alpha
            
            # Combina sticker com background usando alfa
            for c in range(3):
                background[y1:y2, x1:x2, c] = (
                    alpha * sticker[:, :, c] +
                    bg_alpha * background[y1:y2, x1:x2, c]
                )
        else:
            # Sem canal alfa, aplica diretamente
            background[y1:y2, x1:x2] = sticker[:, :, :3]
            
        return background
