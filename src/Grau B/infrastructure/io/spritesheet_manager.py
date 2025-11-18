"""
Gerenciador de spritesheets animados.

Permite carregar e animar spritesheets com múltiplos frames.
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import time


class AnimatedSprite:
    """Representa um sprite animado."""
    
    def __init__(
        self, 
        spritesheet: np.ndarray, 
        frame_width: int, 
        frame_height: int,
        fps: int = 10,
        loop: bool = True
    ):
        """
        Inicializa sprite animado.
        
        Args:
            spritesheet: Imagem completa do spritesheet
            frame_width: Largura de cada frame
            frame_height: Altura de cada frame
            fps: Frames por segundo da animação
            loop: Se a animação deve repetir
        """
        self.spritesheet = spritesheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.fps = fps
        self.loop = loop
        
        # Extrai frames do spritesheet
        self.frames = self._extract_frames()
        self.current_frame = 0
        self.last_update = time.time()
        self.frame_duration = 1.0 / fps
        
    def _extract_frames(self) -> List[np.ndarray]:
        """
        Extrai frames individuais do spritesheet.
        
        Returns:
            Lista de frames
        """
        frames = []
        sheet_height, sheet_width = self.spritesheet.shape[:2]
        
        # Calcula quantos frames cabem horizontalmente
        num_frames = sheet_width // self.frame_width
        
        for i in range(num_frames):
            x = i * self.frame_width
            frame = self.spritesheet[0:self.frame_height, x:x+self.frame_width]
            frames.append(frame)
            
        return frames
    
    def get_current_frame(self) -> np.ndarray:
        """
        Retorna o frame atual da animação.
        
        Returns:
            Frame atual
        """
        current_time = time.time()
        
        # Atualiza frame se passou tempo suficiente
        if current_time - self.last_update >= self.frame_duration:
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    
            self.last_update = current_time
            
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reinicia a animação."""
        self.current_frame = 0
        self.last_update = time.time()


class SpritesheetManager:
    """
    Gerencia spritesheets animados.
    """
    
    def __init__(self):
        """Inicializa gerenciador de spritesheets."""
        self.spritesheets: Dict[str, AnimatedSprite] = {}
        
    def load_spritesheet(
        self, 
        name: str, 
        path: str, 
        frame_width: int, 
        frame_height: int,
        fps: int = 10,
        loop: bool = True
    ) -> bool:
        """
        Carrega spritesheet do disco.
        
        Args:
            name: Nome identificador do spritesheet
            path: Caminho do arquivo PNG
            frame_width: Largura de cada frame
            frame_height: Altura de cada frame
            fps: Frames por segundo
            loop: Se a animação repete
            
        Returns:
            True se carregou com sucesso
        """
        if not Path(path).exists():
            print(f"⚠️ Spritesheet não encontrado: {path}")
            return False
            
        # Carrega com canal alfa
        spritesheet_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        
        if spritesheet_img is None:
            print(f"❌ Erro ao carregar spritesheet: {path}")
            return False
            
        # Cria sprite animado
        sprite = AnimatedSprite(
            spritesheet_img, 
            frame_width, 
            frame_height,
            fps,
            loop
        )
        
        self.spritesheets[name] = sprite
        print(f"✅ Spritesheet '{name}' carregado: {len(sprite.frames)} frames @ {fps}fps")
        
        return True
    
    def get_current_frame(self, name: str) -> Optional[np.ndarray]:
        """
        Retorna frame atual de um spritesheet.
        
        Args:
            name: Nome do spritesheet
            
        Returns:
            Frame atual ou None
        """
        if name not in self.spritesheets:
            return None
            
        return self.spritesheets[name].get_current_frame()
    
    def reset_animation(self, name: str):
        """
        Reinicia animação de um spritesheet.
        
        Args:
            name: Nome do spritesheet
        """
        if name in self.spritesheets:
            self.spritesheets[name].reset()
