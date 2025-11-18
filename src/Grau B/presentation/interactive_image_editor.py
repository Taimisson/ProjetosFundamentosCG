"""
Editor interativo de imagens.

Permite editar imagens estáticas com filtros em tempo real.
"""

import cv2
import numpy as np
from typing import Dict, Optional, Callable
from pathlib import Path

from domain.interfaces.image_processor import ImageProcessorInterface
from infrastructure.io.sticker_manager import StickerManager


class InteractiveImageEditor:
    """
    Editor interativo de imagens com preview em tempo real.
    
    Permite aplicar filtros e stickers usando teclas de atalho.
    """
    
    def __init__(self):
        """Inicializa editor interativo."""
        self.processors: Dict[str, ImageProcessorInterface] = {}
        self.active_processor: Optional[str] = None
        self.sticker_manager = StickerManager()
        self.original_image: Optional[np.ndarray] = None
        self.save_counter = 0
        self.mouse_x = 0
        self.mouse_y = 0
        
        # Carrega stickers disponíveis
        self._load_stickers()
        
    def _load_stickers(self):
        """
        Carrega stickers da pasta assets/stickers.
        
        Suporta múltiplos formatos: PNG (recomendado para transparência), JPG, GIF
        Tenta carregar automaticamente qualquer arquivo de imagem encontrado.
        """
        stickers_dir = Path("assets/stickers")
        if not stickers_dir.exists():
            print("⚠️  Pasta de stickers não encontrada. Funcionalidade desabilitada.")
            return
        
        # Mapeamento padrão (nomes específicos)
        # Usando teclas numéricas para evitar conflito com filtros
        sticker_mapping = {
            '1': 'bongo',         # Bongo
            '2': 'doguinho',      # Cachorrinho
            '3': 'duvida',        # Dúvida
            '4': 'gatinho',       # Gatinho
            '5': 'gato',          # Gato
            '6': 'gremio',        # Grêmio
            '7': 'leao',          # Leão
            '8': 'moodle',        # Moodle
            '9': 'muehehe',       # Risada
            '0': 'peixe',         # Peixe
        }
        
        # Extensões suportadas (PNG recomendado para transparência)
        supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        
        print(f"\n🎭 Carregando stickers de: {stickers_dir}")
        loaded_count = 0
        
        for key, base_name in sticker_mapping.items():
            # Tenta carregar com diferentes extensões
            found = False
            for ext in supported_extensions:
                sticker_path = stickers_dir / f"{base_name}{ext}"
                if sticker_path.exists():
                    if self.sticker_manager.load_sticker(key, str(sticker_path)):
                        print(f"   ✅ '{key.upper()}' -> {sticker_path.name}")
                        loaded_count += 1
                        found = True
                        break
            
            if not found:
                print(f"   ⚠️  '{key.upper()}' -> Nenhum arquivo encontrado ({base_name}.*)")
        
        if loaded_count > 0:
            print(f"✨ Total: {loaded_count} stickers carregados!\n")
        else:
            print("⚠️  Nenhum sticker carregado. Verifique a pasta assets/stickers/\n")
        
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
        print("📸 MODO FOTO - EDITOR INTERATIVO")
        print("=" * 50)
        print("\n🎨 FILTROS DISPONÍVEIS:")
        print("-" * 50)
        
        for key, info in self.processors.items():
            print(f"  {key.upper()}: {info['name']}")
            
        print("\n🎭 STICKERS (clique na imagem, depois pressione número):")
        print("-" * 50)
        print("  1: Cachorro 🐶   2: CatSoquinho 😸  3: Dog 🐕")
        print("  4: Gatinho 🐱    5: Grêmio ⚽       6: Kabum 💥")
        print("  7: Moodle 📚     8: Muehahaa 😈     9: Peixe 🐠")
        print("  0: WhatsApp 💬")
            
        print("\n⚙️  COMANDOS:")
        print("-" * 50)
        print("  R: Remover filtro ativo")
        print("  C: Limpar todos os stickers")
        print("  Q: Salvar imagem atual")
        print("  F: Finalizar edição")
        print("  CLICK: Adicionar sticker selecionado")
        print("=" * 50)
        
    def edit_image(self, image_path: str):
        """
        Abre editor interativo para imagem.
        
        Args:
            image_path: Caminho da imagem a editar
        """
        # Carrega imagem
        if not Path(image_path).exists():
            print(f"❌ Erro: Arquivo não encontrado: {image_path}")
            return
            
        self.original_image = cv2.imread(image_path)
        if self.original_image is None:
            print(f"❌ Erro ao carregar imagem: {image_path}")
            return
            
        self.display_instructions()
        
        # Cria janela
        window_name = "Imagem - Editada (Pressione F para sair)"
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self._mouse_callback)
        
        # Loop de edição
        while True:
            # Frame atual
            frame = self._apply_current_processing(self.original_image.copy())
            
            # Exibe
            cv2.imshow(window_name, frame)
            
            # Aguarda tecla
            key = cv2.waitKey(1) & 0xFF
            
            # Processa tecla
            if not self._handle_key(key, frame):
                break
                
        cv2.destroyAllWindows()
        
    def _mouse_callback(self, event, x, y, flags, param):
        """
        Callback para eventos do mouse.
        
        Args:
            event: Tipo de evento
            x: Coordenada X
            y: Coordenada Y
            flags: Flags adicionais
            param: Parâmetros extras
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            # Salva posição do mouse
            self.mouse_x = x
            self.mouse_y = y
            print(f"🖱️  Click em ({x}, {y})")
        
    def _apply_current_processing(self, frame: np.ndarray) -> np.ndarray:
        """
        Aplica processamento atual no frame.
        
        Args:
            frame: Frame original
            
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
                name="temp"
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
        
        # Exibe filtro ativo
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
            
        return frame
        
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
            print("✅ Edição finalizada.")
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
            
        # Salvar (Q)
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
            # Adiciona sticker na última posição do mouse
            self.sticker_manager.add_sticker(key_char, self.mouse_x, self.mouse_y)
            print(f"🎭 Sticker '{key_char.upper()}' adicionado em ({self.mouse_x}, {self.mouse_y})")
            return True
            
        return True
        
    def _save_frame(self, frame: np.ndarray):
        """
        Salva frame atual.
        
        Args:
            frame: Frame a salvar
        """
        output_dir = Path("assets/images/output/edited")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f"imagem_editada_{self.save_counter}.png"
        cv2.imwrite(str(output_path), frame)
        
        print(f"💾 Imagem salva: {output_path}")
        self.save_counter += 1
