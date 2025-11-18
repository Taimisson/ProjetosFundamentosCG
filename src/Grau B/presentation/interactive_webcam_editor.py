"""
Editor interativo de vídeo da webcam.

Permite aplicar filtros em tempo real na webcam.
"""

import cv2
import numpy as np
from typing import Dict, Optional
from pathlib import Path

from domain.interfaces.image_processor import ImageProcessorInterface
from infrastructure.io.webcam_capture import WebcamCapture
from infrastructure.io.sticker_manager import StickerManager


class InteractiveWebcamEditor:
    """
    Editor interativo de vídeo da webcam com filtros em tempo real.
    
    Permite aplicar filtros e stickers na webcam usando teclas de atalho.
    """
    
    def __init__(self, camera_index: int = 0):
        """
        Inicializa editor de webcam.
        
        Args:
            camera_index: Índice da câmera (0 para padrão)
        """
        self.webcam = WebcamCapture(camera_index)
        self.processors: Dict[str, ImageProcessorInterface] = {}
        self.active_processor: Optional[str] = None
        self.sticker_manager = StickerManager()
        self.save_counter = 0
        self.mouse_x = 0
        self.mouse_y = 0
        
        # Carrega stickers disponíveis
        self._load_stickers()
        
    def _load_stickers(self):
        """Carrega stickers da pasta assets/stickers."""
        stickers_dir = Path("assets/stickers")
        if not stickers_dir.exists():
            print("⚠️  Pasta de stickers não encontrada.")
            return
            
        sticker_mapping = {
            '1': 'bongo',
            '2': 'doguinho',
            '3': 'duvida',
            '4': 'gatinho',
            '5': 'gato',
            '6': 'gremio',
            '7': 'leao',
            '8': 'moodle',
            '9': 'muehehe',
            '0': 'peixe',
        }
        
        supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        
        print(f"\n🎭 Carregando stickers de: {stickers_dir}")
        loaded_count = 0
        
        for key, base_name in sticker_mapping.items():
            found = False
            for ext in supported_extensions:
                sticker_path = stickers_dir / f"{base_name}{ext}"
                if sticker_path.exists():
                    if self.sticker_manager.load_sticker(key, str(sticker_path)):
                        print(f"   ✅ '{key}' -> {sticker_path.name}")
                        loaded_count += 1
                        found = True
                        break
            
            if not found:
                print(f"   ⚠️  '{key}' -> Não encontrado ({base_name}.*)")
        
        if loaded_count > 0:
            print(f"✨ Total: {loaded_count} stickers carregados!\n")
        else:
            print("⚠️  Nenhum sticker foi carregado.\n")
        
    def register_processor(self, key: str, name: str, processor: ImageProcessorInterface):
        """
        Registra processador de imagem para uma tecla.
        
        Args:
            key: Tecla de atalho (ex: 'b' para blur)
            name: Nome descritivo do filtro
            processor: Processador de imagem
        """
        self.processors[key] = {
            'name': name,
            'processor': processor,
            'active': False
        }
        
    def display_instructions(self):
        """Exibe instruções de uso."""
        print("\n" + "=" * 50)
        print("📹 MODO VÍDEO - WEBCAM INTERATIVA")
        print("=" * 50)
        print("\n🎨 FILTROS DISPONÍVEIS:")
        print("-" * 50)
        
        for key, info in self.processors.items():
            print(f"  {key.upper()}: {info['name']}")
            
        print("\n🎭 STICKERS (clique na webcam, depois pressione número):")
        print("-" * 50)
        print("  1: Bongo 🥁       2: Doguinho 🐶   3: Dúvida ❓")
        print("  4: Gatinho 🐱    5: Gato 😺        6: Grêmio ⚽")
        print("  7: Leão 🦁       8: Moodle 📚      9: Muehehe 😆")
        print("  0: Peixe 🐠")
            
        print("\n⚙️  COMANDOS:")
        print("-" * 50)
        print("  R: Remover filtro ativo")
        print("  C: Limpar todos os stickers")
        print("  Q: Capturar screenshot")
        print("  F: Finalizar (ou ESC)")
        print("=" * 50)
        
    def start_editing(self):
        """Inicia edição de vídeo da webcam."""
        # Inicia captura
        if not self.webcam.start():
            return
            
        self.display_instructions()
        
        # Cria janela
        window_name = "Webcam - Editada (Pressione F para sair)"
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self._mouse_callback)
        
        try:
            # Loop de captura
            while True:
                # Captura frame
                frame = self.webcam.read_frame()
                if frame is None:
                    break
                    
                # Processa frame
                processed_frame = self._apply_current_processing(frame)
                
                # Exibe
                cv2.imshow(window_name, processed_frame)
                
                # Aguarda tecla
                key = cv2.waitKey(1) & 0xFF
                
                # Processa tecla
                if not self._handle_key(key, processed_frame):
                    break
                    
        finally:
            # Libera recursos
            self.webcam.release()
            cv2.destroyAllWindows()
            
    def _mouse_callback(self, event, x, y, flags, param):
        """Callback para eventos do mouse."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_x = x
            self.mouse_y = y
            
    def _apply_current_processing(self, frame: np.ndarray) -> np.ndarray:
        """
        Aplica processamento atual no frame.
        
        Args:
            frame: Frame original da webcam
            
        Returns:
            Frame processado
        """
        # Aplica filtro ativo
        if self.active_processor:
            processor_info = self.processors[self.active_processor]
            processor = processor_info['processor']
            
            # Cria Image entity temporário
            from domain.entities.image import Image
            temp_image = Image(
                data=frame,
                width=frame.shape[1],
                height=frame.shape[0],
                channels=frame.shape[2] if len(frame.shape) > 2 else 1,
                name="webcam"
            )
            
            # Processa
            processed = processor.process(temp_image)
            frame = processed.data
            
            # Converte para 3 canais se necessário
            if len(frame.shape) == 2:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            elif frame.dtype == np.float64:
                frame = np.uint8(np.clip(frame, 0, 255))
                
        # Aplica stickers
        frame = self.sticker_manager.apply_stickers(frame)
        
        # Overlay de informações
        self._draw_overlay(frame)
        
        return frame
        
    def _draw_overlay(self, frame: np.ndarray):
        """
        Desenha overlay de informações no frame.
        
        Args:
            frame: Frame a modificar
        """
        # Filtro ativo
        if self.active_processor:
            filter_name = self.processors[self.active_processor]['name']
            cv2.putText(
                frame, 
                f"Filtro: {filter_name}", 
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
        else:
            cv2.putText(
                frame, 
                "Sem filtro", 
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (200, 200, 200),
                2
            )
            
        # Indicador de gravação
        cv2.circle(frame, (frame.shape[1] - 30, 30), 10, (0, 0, 255), -1)
        cv2.putText(
            frame,
            "REC",
            (frame.shape[1] - 70, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2
        )
        
    def _handle_key(self, key: int, current_frame: np.ndarray) -> bool:
        """
        Processa tecla pressionada.
        
        Args:
            key: Código da tecla
            current_frame: Frame atual para salvar
            
        Returns:
            True para continuar, False para sair
        """
        key_char = chr(key) if key < 256 else ''
        
        # Finalizar (F ou ESC)
        if key_char == 'f' or key == 27:
            print("✅ Captura finalizada.")
            return False
            
        # Remover filtro (R)
        if key_char == 'r':
            self.active_processor = None
            print("🔄 Filtro removido.")
            return True
            
        # Limpar stickers (C)
        if key_char == 'c':
            self.sticker_manager.clear_stickers()
            print("🧹 Stickers removidos.")
            return True
            
        # Capturar screenshot (Q)
        if key_char == 'q':
            self._save_frame(current_frame)
            return True
            
        # Ativar filtro
        if key_char in self.processors:
            # Desativa outros filtros
            for k in self.processors:
                self.processors[k]['active'] = False
                
            # Ativa filtro selecionado
            self.processors[key_char]['active'] = True
            self.active_processor = key_char
            
            filter_name = self.processors[key_char]['name']
            print(f"✨ Filtro ativado: {filter_name}")
            return True
            
        # Adicionar sticker (teclas numéricas 0-9)
        sticker_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if key_char in sticker_keys:
            self.sticker_manager.add_sticker(key_char, self.mouse_x, self.mouse_y)
            print(f"🎭 Sticker '{key_char}' adicionado na posição ({self.mouse_x}, {self.mouse_y})")
            return True
            
        return True
        
    def _save_frame(self, frame: np.ndarray):
        """
        Salva frame atual (screenshot).
        
        Args:
            frame: Frame a salvar
        """
        output_dir = Path("assets/images/output/webcam")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f"webcam_editada_{self.save_counter}.png"
        cv2.imwrite(str(output_path), frame)
        
        print(f"📸 Screenshot salvo: {output_path}")
        self.save_counter += 1
