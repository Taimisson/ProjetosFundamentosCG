"""
Sistema de sobreposição de stickers animados sobre faces detectadas.

Cria efeito tipo Instagram com múltiplos sprites animados.
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path

from infrastructure.face_detection import FaceDetector, FacePoint
from infrastructure.io.spritesheet_manager import SpritesheetManager


class AnimatedStickerOverlay:
    """
    Sobrepõe stickers animados sobre pontos faciais detectados.
    
    Efeito tipo filtro do Instagram com múltiplas animações.
    """
    
    def __init__(self):
        """Inicializa sistema de overlay de stickers animados."""
        self.face_detector = FaceDetector()
        self.spritesheet_manager = SpritesheetManager()
        self.enabled = False
        
        # Configuração de quais pontos receberão stickers
        self.sticker_points = [
            "olho_esquerdo",
            "olho_direito",
            "nariz",
            "bochecha_esquerda",
            "bochecha_direita",
            "testa",
            "canto_esq_superior",
            "canto_dir_superior"
        ]
        
        # Escala dos stickers (proporção do tamanho da face)
        self.sticker_scale = 0.20  # 20% do tamanho da face
        
    def load_spritesheet(
        self, 
        spritesheet_path: str,
        frame_width: int = 32,
        frame_height: int = 32,
        fps: int = 12
    ) -> bool:
        """
        Carrega spritesheet animado.
        
        Args:
            spritesheet_path: Caminho do spritesheet
            frame_width: Largura de cada frame
            frame_height: Altura de cada frame
            fps: Frames por segundo
            
        Returns:
            True se carregou com sucesso
        """
        success = self.spritesheet_manager.load_spritesheet(
            name="main_sprite",
            path=spritesheet_path,
            frame_width=frame_width,
            frame_height=frame_height,
            fps=fps,
            loop=True
        )
        
        if success:
            self.enabled = True
            print(f"🎭 Stickers animados habilitados!")
        
        return success
    
    def _overlay_sprite(
        self,
        background: np.ndarray,
        sprite: np.ndarray,
        position: Tuple[int, int],
        scale: float = 1.0
    ) -> np.ndarray:
        """
        Sobrepõe sprite sobre background com transparência.
        
        Args:
            background: Imagem de fundo
            sprite: Sprite com canal alfa
            position: Posição (x, y) do centro do sprite
            scale: Escala do sprite
            
        Returns:
            Imagem com sprite sobreposto
        """
        x_center, y_center = position
        
        # Redimensiona sprite se necessário
        if scale != 1.0:
            new_width = int(sprite.shape[1] * scale)
            new_height = int(sprite.shape[0] * scale)
            sprite = cv2.resize(sprite, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        sprite_h, sprite_w = sprite.shape[:2]
        
        # Calcula posição do canto superior esquerdo
        x = x_center - sprite_w // 2
        y = y_center - sprite_h // 2
        
        # Verifica limites
        bg_h, bg_w = background.shape[:2]
        
        if x >= bg_w or y >= bg_h or x + sprite_w <= 0 or y + sprite_h <= 0:
            return background  # Sprite fora da imagem
        
        # Ajusta recortes se sprite estiver parcialmente fora
        sprite_x1 = max(0, -x)
        sprite_y1 = max(0, -y)
        sprite_x2 = min(sprite_w, bg_w - x)
        sprite_y2 = min(sprite_h, bg_h - y)
        
        bg_x1 = max(0, x)
        bg_y1 = max(0, y)
        bg_x2 = bg_x1 + (sprite_x2 - sprite_x1)
        bg_y2 = bg_y1 + (sprite_y2 - sprite_y1)
        
        # Recorta sprite e área de fundo
        sprite_crop = sprite[sprite_y1:sprite_y2, sprite_x1:sprite_x2]
        bg_crop = background[bg_y1:bg_y2, bg_x1:bg_x2]
        
        # Se sprite não tem canal alfa, adiciona um
        if sprite_crop.shape[2] == 3:
            # Sem canal alfa, usa preto como transparente
            alpha = np.all(sprite_crop != [0, 0, 0], axis=-1).astype(float)
            sprite_crop = np.dstack([sprite_crop, alpha * 255])
        
        # Extrai canal alfa e normaliza
        alpha = sprite_crop[:, :, 3] / 255.0
        alpha = np.stack([alpha] * 3, axis=-1)
        
        # Combina com transparência
        blended = (sprite_crop[:, :, :3] * alpha + bg_crop * (1 - alpha)).astype(np.uint8)
        
        # Copia de volta para o background
        result = background.copy()
        result[bg_y1:bg_y2, bg_x1:bg_x2] = blended
        
        return result
    
    def apply(self, image: np.ndarray) -> np.ndarray:
        """
        Aplica stickers animados sobre faces detectadas.
        
        Args:
            image: Imagem BGR de entrada
            
        Returns:
            Imagem com stickers animados
        """
        if not self.enabled:
            return image
        
        # Detecta faces e pontos
        faces_with_points = self.face_detector.detect_with_points(image)
        
        if not faces_with_points:
            return image
        
        result = image.copy()
        
        # Para cada face detectada
        for face_rect, face_points in faces_with_points:
            x, y, w, h = face_rect
            
            # Calcula tamanho do sticker baseado no tamanho da face
            face_size = max(w, h)
            sticker_size_scale = self.sticker_scale * face_size / 64  # 64 = tamanho padrão do frame
            
            # Obtém frame atual da animação
            sprite_frame = self.spritesheet_manager.get_current_frame("main_sprite")
            
            if sprite_frame is None:
                continue
            
            # Aplica sticker em cada ponto de interesse
            for point in face_points:
                if point.name in self.sticker_points:
                    result = self._overlay_sprite(
                        result,
                        sprite_frame,
                        (point.x, point.y),
                        scale=sticker_size_scale
                    )
        
        return result
    
    def toggle(self):
        """Liga/desliga o efeito de stickers animados."""
        self.enabled = not self.enabled
        status = "habilitado" if self.enabled else "desabilitado"
        print(f"🎭 Stickers animados {status}")
    
    def set_sticker_scale(self, scale: float):
        """
        Define escala dos stickers.
        
        Args:
            scale: Escala (0.1 = 10% do tamanho da face)
        """
        self.sticker_scale = max(0.05, min(0.5, scale))
        print(f"📏 Escala dos stickers: {self.sticker_scale:.2f}")
    
    def set_fps(self, fps: int):
        """
        Ajusta velocidade da animação.
        
        Args:
            fps: Frames por segundo
        """
        sprite = self.spritesheet_manager.spritesheets.get("main_sprite")
        if sprite:
            sprite.fps = fps
            sprite.frame_duration = 1.0 / fps
            print(f"⏱️ FPS da animação: {fps}")
