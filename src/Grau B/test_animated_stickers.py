"""
Script de teste para o sistema de stickers animados.

Testa detecção facial e overlay de sprites animados.
"""

import cv2
from pathlib import Path

from infrastructure.io.animated_sticker_overlay import AnimatedStickerOverlay


def test_animated_stickers():
    """Testa sistema de stickers animados na webcam."""
    print("=" * 60)
    print("🎬 TESTE DE STICKERS ANIMADOS")
    print("=" * 60)
    
    # Inicializa sistema de overlay
    overlay = AnimatedStickerOverlay()
    
    # Carrega spritesheet
    spritesheet_path = Path("assets/spritesheets/necromancer_64.png")
    
    if not spritesheet_path.exists():
        print(f"❌ Spritesheet não encontrado: {spritesheet_path}")
        print("\n📁 Certifique-se de que o arquivo existe em:")
        print(f"   {spritesheet_path.absolute()}")
        return
    
    success = overlay.load_spritesheet(
        str(spritesheet_path),
        frame_width=64,
        frame_height=64,
        fps=12
    )
    
    if not success:
        print("❌ Falha ao carregar spritesheet")
        return
    
    print("\n✅ Spritesheet carregado com sucesso!")
    print("\n📹 Abrindo webcam...")
    
    # Abre webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Erro ao abrir webcam")
        return
    
    print("\n" + "=" * 60)
    print("⌨️  CONTROLES:")
    print("-" * 60)
    print("  A: Ligar/Desligar overlay de stickers animados")
    print("  +: Aumentar tamanho dos stickers")
    print("  -: Diminuir tamanho dos stickers")
    print("  [: Diminuir velocidade (FPS)")
    print("  ]: Aumentar velocidade (FPS)")
    print("  Q: Sair")
    print("=" * 60)
    
    window_name = "Teste Stickers Animados (Pressione Q para sair)"
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Erro ao capturar frame")
                break
            
            # Aplica overlay de stickers animados
            processed = overlay.apply(frame)
            
            # Mostra status no canto
            status_text = "ON" if overlay.enabled else "OFF"
            status_color = (0, 255, 0) if overlay.enabled else (0, 0, 255)
            cv2.putText(
                processed,
                f"Animacao: {status_text}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                status_color,
                2
            )
            
            cv2.putText(
                processed,
                f"Escala: {overlay.sticker_scale:.2f}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )
            
            sprite = overlay.spritesheet_manager.spritesheets.get("main_sprite")
            if sprite:
                cv2.putText(
                    processed,
                    f"FPS: {sprite.fps}",
                    (10, 85),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1
                )
            
            # Exibe
            cv2.imshow(window_name, processed)
            
            # Processa teclas
            key = cv2.waitKey(1) & 0xFF
            key_char = chr(key) if key < 256 else ''
            
            if key_char == 'q' or key == 27:
                print("\n✅ Teste finalizado")
                break
            elif key_char == 'a':
                overlay.toggle()
            elif key_char == '+' or key_char == '=':
                overlay.set_sticker_scale(overlay.sticker_scale + 0.02)
            elif key_char == '-' or key_char == '_':
                overlay.set_sticker_scale(overlay.sticker_scale - 0.02)
            elif key_char == '[':
                if sprite:
                    new_fps = max(1, sprite.fps - 2)
                    overlay.set_fps(new_fps)
            elif key_char == ']':
                if sprite:
                    new_fps = min(30, sprite.fps + 2)
                    overlay.set_fps(new_fps)
    
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    test_animated_stickers()
