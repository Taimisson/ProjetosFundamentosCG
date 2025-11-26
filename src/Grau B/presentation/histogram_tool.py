import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

"""
Ferramenta para visualização e análise de histogramas.

Implementa os requisitos:
- Item 4.11: Visualizar histogramas
- Item 4.12: Analisar efeitos da equalização
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from domain.entities.image import Image
from infrastructure.image_processing.histogram import HistogramEqualizer


class HistogramTool:
    """Ferramenta para visualização de histogramas."""
    
    def __init__(self):
        """Inicializa a ferramenta de histogramas."""
        self.output_dir = Path(__file__).parent.parent / "assets/images/output/histograms"
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
    
    def plot_histogram_comparison(
        self, 
        image_path: str,
        method: str = "rgb"
    ) -> str:
        """
        Plota comparação de histograma original vs equalizado (Item 4.11 e 4.12).
        
        Args:
            image_path: Caminho da imagem de entrada
            method: Método de equalização ('rgb', 'hsv', 'ycrcb')
            
        Returns:
            Caminho do gráfico salvo
        """
        print(f"\n📊 Gerando visualização de histograma ({method.upper()})...")
        
        # Carrega imagem
        image = self._load_image(image_path)
        
        # Escolhe método de equalização
        if method == "rgb":
            equalizer = HistogramEqualizer(color_equalization='all')
            title_suffix = "RGB"
        elif method == "hsv":
            equalizer = HistogramEqualizer(color_equalization='value')
            title_suffix = "HSV"
        elif method == "ycrcb":
            equalizer = HistogramEqualizer(color_equalization='value')
            title_suffix = "YCrCb"
        else:
            raise ValueError(f"Método desconhecido: {method}")
        
        # Aplica equalização
        equalized_image = equalizer.process(image)
        
        # Converte para escala de cinza para análise
        original_gray = cv2.cvtColor(image.data, cv2.COLOR_BGR2GRAY)
        equalized_gray = cv2.cvtColor(equalized_image.data, cv2.COLOR_BGR2GRAY)
        
        # Calcula histogramas
        hist_original = cv2.calcHist([original_gray], [0], None, [256], [0, 256])
        hist_equalized = cv2.calcHist([equalized_gray], [0], None, [256], [0, 256])
        
        # Cria figura com 4 subplots
        fig = plt.figure(figsize=(14, 10))
        
        # Subplot 1: Imagem Original
        plt.subplot(2, 2, 1)
        plt.imshow(cv2.cvtColor(image.data, cv2.COLOR_BGR2RGB))
        plt.title(f"Imagem Original", fontsize=12, fontweight='bold')
        plt.axis('off')
        
        # Subplot 2: Histograma Original
        plt.subplot(2, 2, 2)
        plt.plot(hist_original, color='black', linewidth=2)
        plt.title(f"Histograma Original", fontsize=12, fontweight='bold')
        plt.xlabel("Intensidade de Pixel")
        plt.ylabel("Frequência")
        plt.xlim([0, 256])
        plt.grid(True, alpha=0.3)
        
        # Subplot 3: Imagem Equalizada
        plt.subplot(2, 2, 3)
        plt.imshow(cv2.cvtColor(equalized_image.data, cv2.COLOR_BGR2RGB))
        plt.title(f"Imagem Equalizada ({title_suffix})", fontsize=12, fontweight='bold')
        plt.axis('off')
        
        # Subplot 4: Histograma Equalizado
        plt.subplot(2, 2, 4)
        plt.plot(hist_equalized, color='blue', linewidth=2)
        plt.title(f"Histograma Equalizado", fontsize=12, fontweight='bold')
        plt.xlabel("Intensidade de Pixel")
        plt.ylabel("Frequência")
        plt.xlim([0, 256])
        plt.grid(True, alpha=0.3)
        
        # Adiciona título geral
        fig.suptitle(
            f"Análise de Equalização de Histograma - Método {title_suffix}",
            fontsize=14,
            fontweight='bold',
            y=0.98
        )
        
        plt.tight_layout()
        
        # Salva
        output_path = self.output_dir / f"histograma_{method}.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Histograma salvo em: {output_path}")
        return str(output_path)
    
    def plot_rgb_histograms(self, image_path: str) -> str:
        """
        Plota histogramas separados para canais RGB.
        
        Args:
            image_path: Caminho da imagem de entrada
            
        Returns:
            Caminho do gráfico salvo
        """
        print("\n📊 Gerando histogramas RGB...")
        
        # Carrega imagem
        image = self._load_image(image_path)
        
        # Separa canais
        b, g, r = cv2.split(image.data)
        
        # Calcula histogramas
        hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
        hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])
        
        # Cria figura
        fig = plt.figure(figsize=(14, 10))
        
        # Subplot 1: Imagem Original
        plt.subplot(2, 2, 1)
        plt.imshow(cv2.cvtColor(image.data, cv2.COLOR_BGR2RGB))
        plt.title("Imagem Original", fontsize=12, fontweight='bold')
        plt.axis('off')
        
        # Subplot 2: Histograma Canal Vermelho
        plt.subplot(2, 2, 2)
        plt.plot(hist_r, color='red', linewidth=2)
        plt.title("Canal Vermelho", fontsize=12, fontweight='bold')
        plt.xlabel("Intensidade")
        plt.ylabel("Frequência")
        plt.xlim([0, 256])
        plt.grid(True, alpha=0.3)
        
        # Subplot 3: Histograma Canal Verde
        plt.subplot(2, 2, 3)
        plt.plot(hist_g, color='green', linewidth=2)
        plt.title("Canal Verde", fontsize=12, fontweight='bold')
        plt.xlabel("Intensidade")
        plt.ylabel("Frequência")
        plt.xlim([0, 256])
        plt.grid(True, alpha=0.3)
        
        # Subplot 4: Histograma Canal Azul
        plt.subplot(2, 2, 4)
        plt.plot(hist_b, color='blue', linewidth=2)
        plt.title("Canal Azul", fontsize=12, fontweight='bold')
        plt.xlabel("Intensidade")
        plt.ylabel("Frequência")
        plt.xlim([0, 256])
        plt.grid(True, alpha=0.3)
        
        # Título geral
        fig.suptitle(
            "Análise de Histogramas por Canal RGB",
            fontsize=14,
            fontweight='bold',
            y=0.98
        )
        
        plt.tight_layout()
        
        # Salva
        output_path = self.output_dir / "histograma_rgb_canais.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Histograma RGB salvo em: {output_path}")
        return str(output_path)
    
    def generate_all_histograms(self, image_path: str = "D:\\Projetos\\ProjetosFundamentosCG\\src\\Grau B\\assets\\images\\input\\baboon.png"):
        """
        Gera todos os histogramas de uma vez.
        
        Args:
            image_path: Caminho da imagem de entrada
        """
        print("=" * 70)
        print("📊 GERADOR DE HISTOGRAMAS")
        print("=" * 70)
        print(f"\nImagem de entrada: {image_path}\n")
        
        try:
            # Gera histogramas
            self.plot_histogram_comparison(image_path, method="rgb")
            self.plot_histogram_comparison(image_path, method="hsv")
            self.plot_histogram_comparison(image_path, method="ycrcb")
            self.plot_rgb_histograms(image_path)
            
            print("\n" + "=" * 70)
            print("✅ TODOS OS HISTOGRAMAS FORAM GERADOS COM SUCESSO!")
            print("=" * 70)
            print(f"\nGráficos salvos em: {self.output_dir}")
            print("\nArquivos gerados:")
            print("  - histograma_rgb.png")
            print("  - histograma_hsv.png")
            print("  - histograma_ycrcb.png")
            print("  - histograma_rgb_canais.png")
            
        except Exception as e:
            print(f"\n❌ Erro ao gerar histogramas: {e}")
            raise


if __name__ == "__main__":
    # Testa a ferramenta
    tool = HistogramTool()
    tool.generate_all_histograms(image_path="D:/Projetos/ProjetosFundamentosCG/src/Grau B/assets/images/input/baboon.png")
