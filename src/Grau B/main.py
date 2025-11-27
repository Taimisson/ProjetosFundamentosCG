"""
Arquivo principal para executar a aplicação.

Sistema de Processamento de Imagens com 3 modos:
1. CLI - Menu tradicional (aplicar filtro e salvar)
2. FOTO - Editor interativo de imagens (tempo real)
3. VÍDEO - Editor de webcam em tempo real
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
from infrastructure.image_processing.color_conversion import GrayscaleProcessor
from infrastructure.image_processing.thresholding import BinaryThresholdProcessor, OtsuThresholdProcessor

# Imports da aplicação
from application.use_cases.apply_filter import ApplyFilterUseCase

# Imports da apresentação
from presentation.interactive_image_editor import InteractiveImageEditor
from presentation.interactive_webcam_editor import InteractiveWebcamEditor


def show_main_menu():
    """Exibe menu principal."""
    print("\n" + "=" * 70)
    print(" " * 10 + "🎨 SISTEMA DE PROCESSAMENTO DE IMAGENS - GRAU B")
    print(" " * 15 + "Fundamentos de Computação Gráfica")
    print("=" * 70)
    print("\n📌 ESCOLHA O MODO DE OPERAÇÃO:")
    print("-" * 70)
    print("  1️⃣  MODO CLI     - Menu tradicional (aplicar e salvar)")
    print("  2️⃣  MODO FOTO    - Editor interativo de imagem (tempo real)")
    print("  3️⃣  MODO VÍDEO   - Editor de webcam (tempo real)")
    print("  4️⃣  HISTOGRAMA   - Gerar gráficos de histograma")
    print("  0️⃣  SAIR         - Encerrar aplicação")
    print("=" * 70)


def modo_cli():
    """Modo CLI tradicional - aplicar filtro e salvar."""
    repository = OpenCVImageRepository()
    apply_filter = ApplyFilterUseCase(repository)
    
    print("\n" + "=" * 60)
    print("MODO CLI - PROCESSAMENTO TRADICIONAL")
    print("=" * 60)
    print("\n📋 Filtros Disponíveis:")
    print("-" * 60)
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
    print("0. Voltar ao menu principal")
    print("=" * 60)
    
    while True:
        print("\n" + "-" * 60)
        choice = input("\n➤ Escolha uma opção (0-12): ").strip()
        
        if choice == '0':
            print("↩️  Voltando ao menu principal...")
            break
        
        if choice not in [str(i) for i in range(1, 13)]:
            print("❌ Opção inválida! Tente novamente.")
            continue
        
        # Solicita caminho da imagem
        image_path = input("\n➤ Digite o caminho da imagem de entrada: ").strip()
        
        if not Path(image_path).exists():
            print(f"❌ Erro: Arquivo '{image_path}' não encontrado!")
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
            print("\n⏳ Processando imagem...")
            result = apply_filter.execute(
                input_path=image_path,
                processor=processor
            )
            
            # Exibe as imagens
            original = repository.load(image_path)
            cv.imshow('Imagem Original', original.data)
            cv.imshow('Imagem Processada', result.data)
            
            print("✅ Processamento concluído!")
            print("👁️  Janelas de imagem abertas. Pressione ESC nas janelas para fechar.")
            
            # Aguarda tecla ESC (código 27) nas janelas
            print("\n⏸️  Aguardando... (Pressione ESC nas janelas de imagem)")
            while True:
                key = cv.waitKey(100) & 0xFF
                if key == 27:  # ESC
                    break
            
            cv.destroyAllWindows()
            
            # Pergunta se deseja salvar
            save = input("\n➤ Deseja salvar a imagem processada? (s/n): ").strip().lower()
            if save == 's':
                # Opção de salvar automaticamente
                auto = input("➤ Salvar na pasta padrão? (s=padrão / n=escolher caminho): ").strip().lower()
                
                if auto == 's':
                    # Salva automaticamente na pasta output
                    output_dir = Path("assets/images/output")
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Gera nome baseado no filtro usado
                    filter_names = {
                        '1': 'mean3x3', '2': 'mean5x5', '3': 'gaussian',
                        '4': 'laplacian', '5': 'sobel_h', '6': 'sobel_v',
                        '7': 'sobel_combined', '8': 'erosion', '9': 'dilation',
                        '10': 'opening', '11': 'closing', '12': 'gradient'
                    }
                    filter_name = filter_names.get(choice, 'processed')
                    
                    # Nome do arquivo original
                    original_name = Path(image_path).stem
                    output_path = output_dir / f"{original_name}_{filter_name}.png"
                    
                    if repository.save(result, str(output_path)):
                        print(f"💾 Imagem salva em: {output_path}")
                    else:
                        print("❌ Erro ao salvar a imagem!")
                else:
                    # Usuário escolhe o caminho
                    output_path = input("➤ Digite o caminho de saída (apenas nome ou caminho completo): ").strip()
                    
                    # Se não tiver extensão, adiciona .png
                    if not output_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                        output_path += '.png'
                    
                    # Se for apenas nome, salva na pasta output
                    if not Path(output_path).is_absolute() and '\\' not in output_path and '/' not in output_path:
                        output_dir = Path("assets/images/output")
                        output_dir.mkdir(parents=True, exist_ok=True)
                        output_path = str(output_dir / output_path)
                    
                    if repository.save(result, output_path):
                        print(f"💾 Imagem salva em: {output_path}")
                    else:
                        print("❌ Erro ao salvar a imagem!")
            
        except Exception as e:
            print(f"\n❌ Erro ao processar imagem: {e}")


def modo_foto():
    """Modo FOTO - editor interativo de imagem."""
    print("\n" + "=" * 60)
    print("MODO FOTO - EDITOR INTERATIVO")
    print("=" * 60)
    
    # Solicita imagem
    image_path = input("\n➤ Digite o caminho da imagem: ").strip()
    
    if not Path(image_path).exists():
        print(f"❌ Erro: Arquivo '{image_path}' não encontrado!")
        return
    
    # Cria editor
    editor = InteractiveImageEditor()
    
    # Registra filtros disponíveis com teclas de atalho
    editor.register_processor('b', 'Gaussian Blur', GaussianFilterProcessor(kernel_size=(15, 15), sigma=0))
    editor.register_processor('m', 'Mean Filter 5x5', MeanFilterProcessor(kernel_size=(5, 5)))
    editor.register_processor('l', 'Laplacian', LaplacianFilterProcessor(kernel_size=3))
    editor.register_processor('s', 'Sobel', SobelFilterProcessor(kernel_size=5, direction='both'))
    editor.register_processor('e', 'Erosion', ErosionProcessor(kernel_size=(5, 5)))
    editor.register_processor('d', 'Dilation', DilationProcessor(kernel_size=(5, 5)))
    editor.register_processor('g', 'Grayscale', GrayscaleProcessor())
    editor.register_processor('t', 'Binary Threshold', BinaryThresholdProcessor(threshold=127))
    editor.register_processor('o', 'Otsu Threshold', OtsuThresholdProcessor())
    editor.register_processor('n', 'Negative', LaplacianFilterProcessor(kernel_size=3))  # Placeholder
    
    # Inicia edição
    editor.edit_image(image_path)


def modo_video():
    """Modo VÍDEO - editor de webcam."""
    print("\n" + "=" * 60)
    print("MODO VÍDEO - WEBCAM INTERATIVA")
    print("=" * 60)
    
    # Cria editor de webcam
    editor = InteractiveWebcamEditor(camera_index=0)
    
    # Registra filtros disponíveis com teclas de atalho
    editor.register_processor('b', 'Gaussian Blur', GaussianFilterProcessor(kernel_size=(15, 15), sigma=0))
    editor.register_processor('m', 'Mean Filter 5x5', MeanFilterProcessor(kernel_size=(5, 5)))
    editor.register_processor('l', 'Laplacian', LaplacianFilterProcessor(kernel_size=3))
    editor.register_processor('s', 'Sobel', SobelFilterProcessor(kernel_size=5, direction='both'))
    editor.register_processor('e', 'Erosion', ErosionProcessor(kernel_size=(5, 5)))
    editor.register_processor('d', 'Dilation', DilationProcessor(kernel_size=(5, 5)))
    editor.register_processor('g', 'Grayscale', GrayscaleProcessor())
    editor.register_processor('t', 'Binary Threshold', BinaryThresholdProcessor(threshold=127))
    editor.register_processor('o', 'Otsu Threshold', OtsuThresholdProcessor())
    editor.register_processor('n', 'Gradient', GradientProcessor(kernel_size=(5, 5)))
    
    # Inicia captura
    editor.start_editing()


def main():
    """Função principal da aplicação."""
    while True:
        show_main_menu()
        
        choice = input("\n➤ Selecione o modo (0-4): ").strip()

        if choice == '0':
            print("\n" + "=" * 70)
            print("👋 Encerrando aplicação... Até logo!")
            print("=" * 70)
            break
        elif choice == '1':
            modo_cli()
        elif choice == '2':
            modo_foto()
        elif choice == '3':
            modo_video()
        elif choice == '4':
            # Integração do generate_requirements.py
            print("\n" + "=" * 60)
            print("MODO ENTREGA - GERAR TODOS OS REQUISITOS OBRIGATÓRIOS")
            print("=" * 60)
            try:
                import importlib.util
                import sys
                from pathlib import Path
                grau_b_dir = Path(__file__).parent
                gen_path = grau_b_dir / "generate_requirements.py"
                if not gen_path.exists():
                    print(f"❌ Erro: Arquivo '{gen_path}' não encontrado!")
                else:
                    spec = importlib.util.spec_from_file_location("generate_requirements", str(gen_path))
                    gen_module = importlib.util.module_from_spec(spec)
                    sys.modules["generate_requirements"] = gen_module
                    spec.loader.exec_module(gen_module)
                    gen_module.main()
            except Exception as e:
                print(f"❌ Erro ao executar generate_requirements: {e}")
        else:
            print("\n❌ Opção inválida! Escolha entre 0 e 4.")


if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
