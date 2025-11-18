"""
Ferramenta para gerar comparações visuais entre filtros.

Implementa os requisitos:
- Item 2.4: Comparação de filtros passa-baixa
- Item 2.10: Comparação de detecção de bordas
- Item 3.9: Comparação de transformações morfológicas
- Item 4.8: Comparação de métodos de limiarização
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple

from domain.entities.image import Image
from infrastructure.image_processing.low_pass_filters import (
    MeanFilterProcessor, GaussianFilterProcessor
)
from infrastructure.image_processing.high_pass_filters import (
    LaplacianFilterProcessor, SobelFilterProcessor
)
from infrastructure.image_processing.morphology import (
    ErosionProcessor, DilationProcessor, OpeningProcessor, ClosingProcessor, GradientProcessor
)
from infrastructure.image_processing.thresholding import (
    BinaryThresholdProcessor, AdaptiveThresholdProcessor, OtsuThresholdProcessor
)


class ComparisonTool:
    """Ferramenta para criar comparações visuais entre filtros."""
    
    def __init__(self):
        """Inicializa a ferramenta de comparação."""
        self.output_dir = Path("assets/images/output/comparisons")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_image(self, image_path: str) -> Image:
        """
        Carrega imagem do disco.
        
        Args:
            image_path: Caminho da imagem
            
        Returns:
            Objeto Image
        """
        img_data = cv2.imread(image_path)
        if img_data is None:
            raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
            
        return Image(
            data=img_data,
            width=img_data.shape[1],
            height=img_data.shape[0],
            channels=img_data.shape[2] if len(img_data.shape) > 2 else 1,
            name=Path(image_path).stem
        )
    
    def _create_comparison_grid(
        self, 
        images: List[np.ndarray], 
        titles: List[str],
        cols: int = 2
    ) -> np.ndarray:
        """
        Cria grid de comparação com imagens lado a lado.
        
        Args:
            images: Lista de imagens numpy
            titles: Títulos para cada imagem
            cols: Número de colunas no grid
            
        Returns:
            Imagem combinada com grid
        """
        n_images = len(images)
        rows = (n_images + cols - 1) // cols
        
        # Garante que todas as imagens têm mesma altura
        max_height = max(img.shape[0] for img in images)
        max_width = max(img.shape[1] for img in images)
        
        # Redimensiona todas as imagens para mesma dimensão
        resized_images = []
        for img in images:
            if len(img.shape) == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            resized = cv2.resize(img, (max_width, max_height))
            resized_images.append(resized)
        
        # Adiciona títulos nas imagens
        titled_images = []
        for img, title in zip(resized_images, titles):
            img_copy = img.copy()
            # Adiciona fundo branco para texto
            cv2.rectangle(img_copy, (0, 0), (max_width, 40), (255, 255, 255), -1)
            # Adiciona texto
            cv2.putText(
                img_copy, title, (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2
            )
            titled_images.append(img_copy)
        
        # Preenche com imagens vazias se necessário
        while len(titled_images) < rows * cols:
            titled_images.append(np.ones_like(titled_images[0]) * 255)
        
        # Cria grid
        grid_rows = []
        for i in range(rows):
            row_images = titled_images[i * cols:(i + 1) * cols]
            grid_rows.append(np.hstack(row_images))
        
        return np.vstack(grid_rows)
    
    def compare_lowpass_filters(self, image_path: str) -> str:
        """
        Compara filtros passa-baixa (Item 2.4).
        
        Args:
            image_path: Caminho da imagem de entrada
            
        Returns:
            Caminho da imagem de comparação salva
        """
        print("\n🔍 Gerando comparação de filtros passa-baixa...")
        
        # Carrega imagem
        image = self._load_image(image_path)
        
        # Aplica filtros
        filters = {
            "Original": None,
            "Mean 3x3": MeanFilterProcessor(kernel_size=(3, 3)),
            "Mean 5x5": MeanFilterProcessor(kernel_size=(5, 5)),
            "Gaussian": GaussianFilterProcessor(kernel_size=(5, 5))
        }
        
        images = []
        titles = []
        
        for title, filter_obj in filters.items():
            if filter_obj is None:
                images.append(image.data)
            else:
                processed = filter_obj.process(image)
                images.append(processed.data)
            titles.append(title)
        
        # Cria grid de comparação
        comparison = self._create_comparison_grid(images, titles, cols=2)
        
        # Salva
        output_path = self.output_dir / "comparacao_passa_baixa.png"
        cv2.imwrite(str(output_path), comparison)
        
        print(f"✅ Comparação salva em: {output_path}")
        return str(output_path)
    
    def compare_edge_detection(self, image_path: str) -> str:
        """
        Compara métodos de detecção de bordas (Item 2.10).
        
        Args:
            image_path: Caminho da imagem de entrada
            
        Returns:
            Caminho da imagem de comparação salva
        """
        print("\n🔍 Gerando comparação de detecção de bordas...")
        
        # Carrega imagem
        image = self._load_image(image_path)
        
        # Aplica filtros
        filters = {
            "Original": None,
            "Laplacian": LaplacianFilterProcessor(),
            "Sobel X": SobelFilterProcessor(direction='x'),
            "Sobel Y": SobelFilterProcessor(direction='y'),
            "Sobel Combined": SobelFilterProcessor(direction='both')
        }
        
        images = []
        titles = []
        
        for title, filter_obj in filters.items():
            if filter_obj is None:
                images.append(image.data)
            else:
                processed = filter_obj.process(image)
                images.append(processed.data)
            titles.append(title)
        
        # Cria grid de comparação (3 colunas para 5 imagens)
        comparison = self._create_comparison_grid(images, titles, cols=3)
        
        # Salva
        output_path = self.output_dir / "comparacao_bordas.png"
        cv2.imwrite(str(output_path), comparison)
        
        print(f"✅ Comparação salva em: {output_path}")
        return str(output_path)
    
    def compare_morphology(self, image_path: str) -> str:
        """
        Compara transformações morfológicas (Item 3.9).
        
        Args:
            image_path: Caminho da imagem de entrada
            
        Returns:
            Caminho da imagem de comparação salva
        """
        print("\n🔍 Gerando comparação de transformações morfológicas...")
        
        # Carrega imagem
        image = self._load_image(image_path)
        
        # Aplica transformações
        filters = {
            "Original": None,
            "Erosion": ErosionProcessor(),
            "Dilation": DilationProcessor(),
            "Opening": OpeningProcessor(),
            "Closing": ClosingProcessor(),
            "Gradient": GradientProcessor()
        }
        
        images = []
        titles = []
        
        for title, filter_obj in filters.items():
            if filter_obj is None:
                images.append(image.data)
            else:
                processed = filter_obj.process(image)
                images.append(processed.data)
            titles.append(title)
        
        # Cria grid de comparação
        comparison = self._create_comparison_grid(images, titles, cols=3)
        
        # Salva
        output_path = self.output_dir / "comparacao_morfologia.png"
        cv2.imwrite(str(output_path), comparison)
        
        print(f"✅ Comparação salva em: {output_path}")
        return str(output_path)
    
    def compare_thresholding(self, image_path: str) -> str:
        """
        Compara métodos de limiarização (Item 4.8).
        
        Args:
            image_path: Caminho da imagem de entrada
            
        Returns:
            Caminho da imagem de comparação salva
        """
        print("\n🔍 Gerando comparação de métodos de limiarização...")
        
        # Carrega imagem
        image = self._load_image(image_path)
        
        # Aplica métodos
        filters = {
            "Original": None,
            "Binary (127)": BinaryThresholdProcessor(threshold=127),
            "Adaptive Mean": AdaptiveThresholdProcessor(method='mean'),
            "Adaptive Gaussian": AdaptiveThresholdProcessor(method='gaussian'),
            "Otsu": OtsuThresholdProcessor()
        }
        
        images = []
        titles = []
        
        for title, filter_obj in filters.items():
            if filter_obj is None:
                images.append(image.data)
            else:
                processed = filter_obj.process(image)
                images.append(processed.data)
            titles.append(title)
        
        # Cria grid de comparação
        comparison = self._create_comparison_grid(images, titles, cols=3)
        
        # Salva
        output_path = self.output_dir / "comparacao_thresholding.png"
        cv2.imwrite(str(output_path), comparison)
        
        print(f"✅ Comparação salva em: {output_path}")
        return str(output_path)
    
    def generate_all_comparisons(self, image_path: str = "assets/images/input/baboon.png"):
        """
        Gera todas as comparações de uma vez.
        
        Args:
            image_path: Caminho da imagem de entrada
        """
        print("=" * 70)
        print("🎨 GERADOR DE COMPARAÇÕES VISUAIS")
        print("=" * 70)
        print(f"\nImagem de entrada: {image_path}\n")
        
        try:
            # Gera todas as comparações
            self.compare_lowpass_filters(image_path)
            self.compare_edge_detection(image_path)
            self.compare_morphology(image_path)
            self.compare_thresholding(image_path)
            
            print("\n" + "=" * 70)
            print("✅ TODAS AS COMPARAÇÕES FORAM GERADAS COM SUCESSO!")
            print("=" * 70)
            print(f"\nImagens salvas em: {self.output_dir}")
            print("\nArquivos gerados:")
            print("  - comparacao_passa_baixa.png")
            print("  - comparacao_bordas.png")
            print("  - comparacao_morfologia.png")
            print("  - comparacao_thresholding.png")
            
        except Exception as e:
            print(f"\n❌ Erro ao gerar comparações: {e}")
            raise


if __name__ == "__main__":
    # Testa a ferramenta
    tool = ComparisonTool()
    tool.generate_all_comparisons()
