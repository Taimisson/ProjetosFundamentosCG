"""
Script para gerar todas as comparações e histogramas obrigatórios.

Executa:
- Comparações visuais (itens 2.4, 2.10, 3.9, 4.8)
- Histogramas (itens 4.11, 4.12)
"""

from presentation.comparison_tool import ComparisonTool
from presentation.histogram_tool import HistogramTool
import os
from pathlib import Path


def main():
    """Gera todos os requisitos obrigatórios."""
    print("\n" + "=" * 70)
    print("🎯 GERADOR DE REQUISITOS OBRIGATÓRIOS - GRAU B")
    print("=" * 70)
    
    # Solicita imagem de teste ao usuário
    while True:
        image_path = input("\n➤ Digite o caminho da imagem de teste para gerar os requisitos: ").strip()
        if not image_path:
            image_path = "assets/images/input/baboon.png"
        if not os.path.exists(image_path):
            print(f"❌ Erro: Arquivo '{image_path}' não encontrado! Informe um caminho válido.")
        else:
            break
    
    # Diretório base do Grau B
    grau_b_dir = Path(__file__).parent
    comparisons_dir = grau_b_dir / "assets/images/output/comparisons"
    histograms_dir = grau_b_dir / "assets/images/output/histograms"
    comparisons_dir.mkdir(parents=True, exist_ok=True)
    histograms_dir.mkdir(parents=True, exist_ok=True)
    
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
    # Mensagem final com caminho absoluto
    print("\n📂 Locais dos arquivos:")
    print(f"   Comparações: {comparisons_dir.resolve()}")
    print(f"   Histogramas: {histograms_dir.resolve()}")
    print("\n✅ Pronto para entrega!\n")


if __name__ == "__main__":
    main()
