"""
Arquivo principal para executar a aplicação.
"""
import cv2 as cv
from pathlib import Path

# Imports da infraestrutura
from infrastructure.io.opencv_repository import OpenCVImageRepository
from infrastructure.image_processing.low_pass_filters import MeanFilterProcessor, GaussianFilterProcessor
from infrastructure.image_processing.high_pass_filters import LaplacianFilterProcessor, SobelFilterProcessor
from infrastructure.image_processing.morphology import (
    ErosionProcessor, DilationProcessor, OpeningProcessor, ClosingProcessor, GradientProcessor
)

# Imports da aplicação
from application.use_cases.apply_filter import ApplyFilterUseCase


def main():
    """Função principal da aplicação."""
    print("=" * 60)
    print("Sistema de Processamento de Imagens - Grau B")
    print("Fundamentos de Computação Gráfica")
    print("=" * 60)
    
    # Inicializa o repositório
    repository = OpenCVImageRepository()
    
    # Inicializa o caso de uso
    apply_filter = ApplyFilterUseCase(repository)
    
    # Menu de opções
    print("\nFiltros Disponíveis:")
    print("1. Filtro de Média 3x3 (Passa-Baixa)")
    print("2. Filtro de Média 5x5 (Passa-Baixa)")
    print("3. Filtro Gaussiano (Passa-Baixa)")
    print("4. Filtro Laplaciano (Passa-Alta)")
    print("5. Filtro Sobel - Horizontal (Passa-Alta)")
    print("6. Filtro Sobel - Vertical (Passa-Alta)")
    print("7. Filtro Sobel - Combinado (Passa-Alta)")
    print("8. Erosão (Morfológica)")
    print("9. Dilatação (Morfológica)")
    print("10. Abertura (Morfológica)")
    print("11. Fechamento (Morfológica)")
    print("12. Gradiente Morfológico")
    print("0. Sair")
    
    while True:
        print("\n" + "-" * 60)
        choice = input("\nEscolha uma opção (0-12): ").strip()
        
        if choice == '0':
            print("\nEncerrando aplicação...")
            break
        
        if choice not in [str(i) for i in range(13)]:
            print("Opção inválida! Tente novamente.")
            continue
        
        # Solicita caminho da imagem
        image_path = input("\nDigite o caminho da imagem de entrada: ").strip()
        
        if not Path(image_path).exists():
            print(f"Erro: Arquivo '{image_path}' não encontrado!")
            continue
        
        # Cria o processador baseado na escolha
        processor = None
        
        if choice == '1':
            processor = MeanFilterProcessor(kernel_size=(3, 3))
        elif choice == '2':
            processor = MeanFilterProcessor(kernel_size=(5, 5))
        elif choice == '3':
            processor = GaussianFilterProcessor(kernel_size=(5, 5), sigma=1.0)
        elif choice == '4':
            processor = LaplacianFilterProcessor(kernel_size=3)
        elif choice == '5':
            processor = SobelFilterProcessor(kernel_size=3, direction='x')
        elif choice == '6':
            processor = SobelFilterProcessor(kernel_size=3, direction='y')
        elif choice == '7':
            processor = SobelFilterProcessor(kernel_size=3, direction='both')
        elif choice == '8':
            processor = ErosionProcessor(kernel_size=(5, 5))
        elif choice == '9':
            processor = DilationProcessor(kernel_size=(5, 5))
        elif choice == '10':
            processor = OpeningProcessor(kernel_size=(5, 5))
        elif choice == '11':
            processor = ClosingProcessor(kernel_size=(5, 5))
        elif choice == '12':
            processor = GradientProcessor(kernel_size=(5, 5))
        
        try:
            # Aplica o filtro
            print("\nProcessando imagem...")
            result = apply_filter.execute(
                input_path=image_path,
                processor=processor
            )
            
            # Exibe as imagens
            original = repository.load(image_path)
            cv.imshow('Imagem Original', original.data)
            cv.imshow('Imagem Processada', result.data)
            
            print("\nProcessamento concluído!")
            print("Pressione qualquer tecla nas janelas de imagem para continuar...")
            
            # Pergunta se deseja salvar
            save = input("\nDeseja salvar a imagem processada? (s/n): ").strip().lower()
            if save == 's':
                output_path = input("Digite o caminho de saída: ").strip()
                if repository.save(result, output_path):
                    print(f"Imagem salva em: {output_path}")
                else:
                    print("Erro ao salvar a imagem!")
            
            cv.waitKey(0)
            cv.destroyAllWindows()
            
        except Exception as e:
            print(f"\nErro ao processar imagem: {e}")


if __name__ == "__main__":
    main()
