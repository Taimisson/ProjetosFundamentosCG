"""
Script para gerar todas as comparações e histogramas obrigatórios.

Executa:
- Comparações visuais (itens 2.4, 2.10, 3.9, 4.8)
- Histogramas (itens 4.11, 4.12)
"""

from presentation.comparison_tool import ComparisonTool
from presentation.histogram_tool import HistogramTool


def main():
    """Gera todos os requisitos obrigatórios."""
    print("\n" + "=" * 70)
    print("🎯 GERADOR DE REQUISITOS OBRIGATÓRIOS - GRAU B")
    print("=" * 70)
    
    # Imagem padrão de teste
    image_path = "assets/images/input/baboon.png"
    
    # Gera comparações visuais
    print("\n📌 PARTE 1: COMPARAÇÕES VISUAIS\n")
    comparison_tool = ComparisonTool()
    comparison_tool.generate_all_comparisons(image_path)
    
    # Gera histogramas
    print("\n\n📌 PARTE 2: HISTOGRAMAS\n")
    histogram_tool = HistogramTool()
    histogram_tool.generate_all_histograms(image_path)
    
    print("\n\n" + "=" * 70)
    print("🎉 TODOS OS REQUISITOS OBRIGATÓRIOS FORAM GERADOS!")
    print("=" * 70)
    print("\n📂 Locais dos arquivos:")
    print("   Comparações: assets/images/output/comparisons/")
    print("   Histogramas: assets/images/output/histograms/")
    print("\n✅ Pronto para entrega!\n")


if __name__ == "__main__":
    main()
