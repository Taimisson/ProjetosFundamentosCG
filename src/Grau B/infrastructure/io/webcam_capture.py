"""
Módulo de captura de vídeo da webcam.

Implementa funcionalidade de captura em tempo real usando OpenCV.
"""

import cv2
import numpy as np
from typing import Optional, Callable


class WebcamCapture:
    """
    Gerencia captura de vídeo da webcam.
    
    Permite capturar frames em tempo real e aplicar processamento.
    """
    
    def __init__(self, camera_index: int = 0):
        """
        Inicializa captura da webcam.
        
        Args:
            camera_index: Índice da câmera (0 para câmera padrão)
        """
        self.camera_index = camera_index
        self.capture: Optional[cv2.VideoCapture] = None
        
    def start(self) -> bool:
        """
        Inicia captura da webcam.
        
        Returns:
            True se iniciou com sucesso, False caso contrário
        """
        self.capture = cv2.VideoCapture(self.camera_index)
        if not self.capture.isOpened():
            print("❌ Erro: Não foi possível abrir a câmera.")
            return False
        return True
    
    def read_frame(self) -> Optional[np.ndarray]:
        """
        Captura um frame da webcam.
        
        Returns:
            Frame capturado ou None se houver erro
        """
        if self.capture is None:
            return None
            
        ret, frame = self.capture.read()
        if not ret:
            print("❌ Erro ao capturar frame.")
            return None
            
        return frame
    
    def release(self):
        """Libera recursos da webcam."""
        if self.capture is not None:
            self.capture.release()
            self.capture = None
            
    def __enter__(self):
        """Context manager: inicia captura."""
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager: libera recursos."""
        self.release()
