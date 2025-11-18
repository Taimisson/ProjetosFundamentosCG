"""
Filtro de cachorro estilo Snapchat.

Sobrepõe imagem completa de cachorro (orelhas + nariz) mapeada no rosto detectado.
"""

import cv2
import numpy as np
from typing import Tuple, Optional
from pathlib import Path

from infrastructure.face_detection import FaceDetector


class DogFilterOverlay:
    """
    Filtro de cachorro que mapeia imagem completa no rosto.
    
    Efeito tipo filtro do Snapchat/Instagram.
    """
    
    def __init__(self):
        """Inicializa filtro de cachorro."""
        self.face_detector = FaceDetector()
        self.enabled = False
        
        # Imagem completa do filtro (orelhas + nariz)
        self.dog_overlay: Optional[np.ndarray] = None
        
    def load_filter(self, filter_path: str) -> bool:
        """
        Carrega imagem do filtro de cachorro.
        
        Args:
            filter_path: Caminho da imagem PNG com transparência
            
        Returns:
            True se carregou com sucesso
        """
        try:
            # Carrega imagem com canal alfa (RGBA)
            self.dog_overlay = cv2.imread(filter_path, cv2.IMREAD_UNCHANGED)
            
            if self.dog_overlay is None:
                print(f"❌ Erro ao carregar filtro: {filter_path}")
                return False
            
            # Verifica se tem canal alfa
            if self.dog_overlay.shape[2] != 4:
                print("⚠️ Imagem deve ter canal alfa (PNG com transparência)")
                return False
            
            self.enabled = True
            print(f"🐶 Filtro de cachorro carregado! ({self.dog_overlay.shape[1]}x{self.dog_overlay.shape[0]})")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar filtro: {e}")
            return False
    
    def apply(self, image: np.ndarray) -> np.ndarray:
        """
        Aplica filtro de cachorro na imagem.
        
        Args:
            image: Imagem de entrada (BGR)
            
        Returns:
            Imagem com filtro aplicado
        """
        if not self.enabled or self.dog_overlay is None:
            return image
        
        # Detecta faces
        faces = self.face_detector.detect_faces(image)
        
        if len(faces) == 0:
            return image
        
        result = image.copy()
        
        # Aplica filtro em cada face detectada
        for face_rect in faces:
            x, y, w, h = face_rect
            
            # Calcula posição e escala do overlay
            # O filtro deve cobrir a face inteira com as orelhas acima
            overlay_width = int(w * 0.95)  # Largura ajustada à face
            overlay_height = int(h * 1.15)  # Altura para incluir orelhas
            
            # Centraliza horizontalmente, mas posiciona verticalmente 
            # para que as orelhas fiquem acima da testa
            overlay_x = x + w // 2
            overlay_y = y + int(h * 0.35)  # Centro vertical ajustado
            
            result = self._overlay_filter(
                result,
                (overlay_x, overlay_y),
                overlay_width,
                overlay_height
            )
        
        return result
    
    def _overlay_filter(
        self,
        background: np.ndarray,
        center_position: Tuple[int, int],
        width: int,
        height: int
    ) -> np.ndarray:
        """
        Sobrepõe filtro completo na posição especificada.
        
        Args:
            background: Imagem de fundo
            center_position: Posição (x, y) do centro
            width: Largura do overlay
            height: Altura do overlay
            
        Returns:
            Imagem com filtro sobreposto
        """
        if self.dog_overlay is None:
            return background
        
        x_center, y_center = center_position
        
        # Redimensiona overlay mantendo proporção
        overlay_resized = cv2.resize(
            self.dog_overlay,
            (width, height),
            interpolation=cv2.INTER_AREA
        )
        
        # Calcula posição do canto superior esquerdo
        x1 = x_center - width // 2
        y1 = y_center - height // 2
        x2 = x1 + width
        y2 = y1 + height
        
        # Verifica limites da imagem
        if x1 >= background.shape[1] or y1 >= background.shape[0]:
            return background
        if x2 <= 0 or y2 <= 0:
            return background
        
        # Ajusta para limites da imagem
        overlay_x1 = max(0, -x1)
        overlay_y1 = max(0, -y1)
        overlay_x2 = width - max(0, x2 - background.shape[1])
        overlay_y2 = height - max(0, y2 - background.shape[0])
        
        bg_x1 = max(0, x1)
        bg_y1 = max(0, y1)
        bg_x2 = min(background.shape[1], x2)
        bg_y2 = min(background.shape[0], y2)
        
        # Extrai região de interesse
        roi = background[bg_y1:bg_y2, bg_x1:bg_x2]
        overlay_crop = overlay_resized[overlay_y1:overlay_y2, overlay_x1:overlay_x2]
        
        if roi.shape[0] == 0 or roi.shape[1] == 0:
            return background
        if overlay_crop.shape[0] == 0 or overlay_crop.shape[1] == 0:
            return background
        
        # Garante que ROI e overlay têm o mesmo tamanho
        if roi.shape[:2] != overlay_crop.shape[:2]:
            return background
        
        # Separa canal alfa
        overlay_bgr = overlay_crop[:, :, :3]
        alpha = overlay_crop[:, :, 3] / 255.0
        
        # Expande alpha para 3 canais
        alpha_3ch = np.stack([alpha, alpha, alpha], axis=2)
        
        # Alpha blending
        blended = (alpha_3ch * overlay_bgr + (1 - alpha_3ch) * roi).astype(np.uint8)
        
        background[bg_y1:bg_y2, bg_x1:bg_x2] = blended
        
        return background
    
    def toggle(self):
        """Liga/desliga filtro."""
        self.enabled = not self.enabled
        status = "habilitado" if self.enabled else "desabilitado"
        print(f"🐶 Filtro de cachorro {status}")
