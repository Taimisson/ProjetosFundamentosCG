"""
Teste do filtro de cachorro estilo Snapchat.

Aplica overlay completo de cachorro sobre faces detectadas via webcam.
"""

import cv2
from pathlib import Path

from infrastructure.io.dog_filter_overlay import DogFilterOverlay


def main():
    """Testa filtro de cachorro com webcam."""
    print("🐶 Iniciando teste do filtro de cachorro...")
    
    # Inicializa filtro
    dog_filter = DogFilterOverlay()
    
    # Carrega imagem do filtro
    filter_path = Path("assets/dog_filter/snapchat.png")
    success = dog_filter.load_filter(str(filter_path))
    
    if not success:
        print("❌ Erro ao carregar filtro")
        return
    
    # Abre webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Erro ao abrir webcam")
        return
    
    print("\n📹 Webcam iniciada!")
    print("Controles:")
    print("  D - Ativar/Desativar filtro de cachorro")
    print("  Q - Sair")
    print()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Aplica filtro de cachorro
        processed = dog_filter.apply(frame)
        
        # Adiciona status
        status_text = "🐶 ATIVO" if dog_filter.enabled else "❌ DESATIVADO"
        cv2.putText(
            processed,
            f"Filtro de Cachorro: {status_text}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0) if dog_filter.enabled else (0, 0, 255),
            2
        )
        
        cv2.putText(
            processed,
            "Pressione D para ativar/desativar | Q para sair",
            (10, processed.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )
        
        # Mostra resultado
        cv2.imshow("Filtro de Cachorro - Estilo Snapchat", processed)
        
        # Captura teclas
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('d') or key == ord('D'):
            dog_filter.toggle()
    
    # Limpa recursos
    cap.release()
    cv2.destroyAllWindows()
    print("\n👋 Aplicação encerrada!")


if __name__ == "__main__":
    main()
