"""
Sistema de detecção facial para aplicação de filtros.

Usa Haar Cascades do OpenCV para detectar faces e pontos faciais.
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path


class FacePoint:
    """Representa um ponto de interesse na face."""
    
    def __init__(self, x: int, y: int, name: str = ""):
        """
        Inicializa ponto facial.
        
        Args:
            x: Coordenada X
            y: Coordenada Y
            name: Nome do ponto (ex: "olho_esquerdo", "nariz")
        """
        self.x = x
        self.y = y
        self.name = name


class FaceDetector:
    """
    Detecta faces e pontos faciais em imagens.
    
    Usa Haar Cascades pré-treinados do OpenCV.
    """
    
    def __init__(self):
        """Inicializa detector facial."""
        # Tenta carregar Haar Cascade para detecção de face
        self.face_cascade = None
        self.eye_cascade = None
        
        # Caminhos possíveis dos Haar Cascades
        cascade_paths = [
            # OpenCV instalado via pip
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml',
            # Caminho local
            'assets/haarcascades/haarcascade_frontalface_default.xml',
        ]
        
        for path in cascade_paths:
            if Path(path).exists():
                self.face_cascade = cv2.CascadeClassifier(path)
                print(f"✅ Haar Cascade carregado: {path}")
                break
        
        # Tenta carregar cascade de olhos
        eye_paths = [
            cv2.data.haarcascades + 'haarcascade_eye.xml',
            'assets/haarcascades/haarcascade_eye.xml',
        ]
        
        for path in eye_paths:
            if Path(path).exists():
                self.eye_cascade = cv2.CascadeClassifier(path)
                break
                
        if self.face_cascade is None:
            print("⚠️ Haar Cascade não encontrado. Usando detecção simples.")
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detecta faces na imagem.
        
        Args:
            image: Imagem BGR
            
        Returns:
            Lista de retângulos (x, y, w, h) das faces detectadas
        """
        if self.face_cascade is None:
            # Sem detector, retorna face "fake" no centro
            h, w = image.shape[:2]
            return [(w//4, h//4, w//2, h//2)]
        
        # Converte para grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detecta faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return faces
    
    def get_face_points(
        self, 
        image: np.ndarray, 
        face_rect: Tuple[int, int, int, int]
    ) -> List[FacePoint]:
        """
        Extrai pontos de interesse de uma face.
        
        Args:
            image: Imagem BGR
            face_rect: Retângulo da face (x, y, w, h)
            
        Returns:
            Lista de pontos faciais
        """
        x, y, w, h = face_rect
        
        # Pontos de interesse calculados geometricamente
        points = []
        
        # Centro da face
        points.append(FacePoint(x + w//2, y + h//2, "centro"))
        
        # Olhos (estimativa geométrica)
        eye_y = y + h//3
        points.append(FacePoint(x + w//3, eye_y, "olho_esquerdo"))
        points.append(FacePoint(x + 2*w//3, eye_y, "olho_direito"))
        
        # Nariz
        points.append(FacePoint(x + w//2, y + 2*h//3, "nariz"))
        
        # Boca
        points.append(FacePoint(x + w//2, y + 5*h//6, "boca"))
        
        # Bochechas
        points.append(FacePoint(x + w//4, y + h//2, "bochecha_esquerda"))
        points.append(FacePoint(x + 3*w//4, y + h//2, "bochecha_direita"))
        
        # Testa
        points.append(FacePoint(x + w//2, y + h//6, "testa"))
        
        # Queixo
        points.append(FacePoint(x + w//2, y + h, "queixo"))
        
        # Cantos da face
        points.append(FacePoint(x + w//8, y + h//3, "canto_esq_superior"))
        points.append(FacePoint(x + 7*w//8, y + h//3, "canto_dir_superior"))
        
        return points
    
    def detect_with_points(
        self, 
        image: np.ndarray
    ) -> List[Tuple[Tuple[int, int, int, int], List[FacePoint]]]:
        """
        Detecta faces e seus pontos de interesse.
        
        Args:
            image: Imagem BGR
            
        Returns:
            Lista de tuplas (face_rect, face_points)
        """
        faces = self.detect_faces(image)
        results = []
        
        for face in faces:
            points = self.get_face_points(image, face)
            results.append((face, points))
        
        return results
