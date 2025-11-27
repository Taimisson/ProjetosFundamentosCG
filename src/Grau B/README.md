# Trabalho Grau B - Processamento de Imagens

Sistema de processamento de imagens desenvolvido em Python utilizando OpenCV, implementando filtros e transformações para a disciplina **Fundamentos de Computação Gráfica**.

> **📝 Nota:** A documentação completa de efeitos dos filtros está em `EFEITOS_FILTROS.md`.

## 👥 Autor
**Nome:** Taimisson de Carvalho Schardosim e Guilherme Lenzi
**Disciplina:** Fundamentos de Computação Gráfica  
**Período:** 2025/1

## 🎯 Objetivo
Implementar sistema completo de processamento de imagens com filtros, transformações morfológicas e operações avançadas, incluindo interfaces interativas para aplicação em tempo real.

## 🏗️ Tecnologias & Dependências
Bibliotecas principais utilizadas:
- **OpenCV** >= 4.8.0 (processamento de imagens)
- **NumPy** >= 1.24.0 (operações matriciais)
- **Matplotlib** >= 3.7.0 (visualização de histogramas)

Requisitos:
- Python 3.13+
- Sistema operacional: Windows/Linux/macOS
- Webcam (opcional, para modo vídeo)

## 📂 Estrutura do Projeto
```
Grau B/
├── domain/                 # Camada de Domínio (Regras de Negócio)
│   ├── entities/          # Entidades do domínio
│   └── interfaces/        # Contratos/Interfaces
├── application/           # Camada de Aplicação (Casos de Uso)
│   └── use_cases/        # Casos de uso específicos
├── infrastructure/        # Camada de Infraestrutura
│   ├── image_processing/ # Implementações de processamento
│   └── io/               # Entrada/Saída de dados
├── presentation/          # Camada de Apresentação (UI/CLI)
├── assets/               # Recursos do projeto
│   ├── images/           # Imagens de teste
│   ├── stickers/         # Stickers PNG com transparência
│   ├── spritesheets/     # Spritesheets para animação
│   └── dog_filter/       # Elementos do filtro de cachorro
├── config/               # Configurações
├── tests/                # Testes unitários
├── main.py               # Ponto de entrada principal
└── README.md             # Esta documentação
```

**Total implementado:** 33 processadores de imagem + 3 modos de operação + Sistema de detecção facial


## 🔧 Instalação
### Opção 1: Ambiente Virtual (Recomendado)
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Opção 2: Instalação Global
```bash
pip install -r requirements.txt
```

## ▶️ Execução
Após instalar as dependências:

### Modo Principal (Menu Interativo)
```bash
python main.py
```
Escolha entre 3 modos:
- **1** = CLI (tradicional, menu com opções)
- **2** = FOTO (editor interativo com teclas)
- **3** = VÍDEO (webcam em tempo real)
- **4** = GERAR HISTOGRAMAS (com image path)


### Descrição dos Modos

#### 🎯 Modo 1: CLI Tradicional
Menu interativo para aplicar filtros e salvar imagens.
```bash
python main.py
# Selecione opção 1: MODO CLI
```

#### 📸 Modo 2: FOTO Interativo
Editor em tempo real com preview instantâneo de filtros.
```bash
python main.py
# Selecione opção 2: MODO FOTO
```

**Teclas de Atalho (Modo FOTO):**
- `B` - Gaussian Blur
- `L` - Laplacian (bordas)
- `S` - Sobel (bordas)
- `E` - Erosão
- `D` - Dilatação
- `G` - Grayscale
- `T` - Threshold binário
- `O` - Otsu threshold
- `R` - Remover filtro
- `Q` - Salvar imagem
- `F` - Finalizar

#### 📹 Modo 3: VÍDEO Webcam
Filtros em tempo real na webcam.
```bash
python main.py
# Selecione opção 3: MODO VÍDEO
```

**Teclas de Atalho (Modo VÍDEO):**
| Tecla | Ação |
|-------|------|
| B, L, S, E, D, G, T, O | Aplicar filtros (mesmos do Modo FOTO) |
| D | Ativar filtro de cachorro (Snapchat) |
| A | Ativar stickers animados no rosto |
| Q | Capturar screenshot |
| F | Finalizar captura |
| ESC | Sair |

## 🛠️ Customizações Rápidas
- **Alterar limiar**: Modificar valores em `infrastructure/image_processing/thresholding.py`
- **Ajustar kernel**: Alterar `kernel_size` nos processadores de filtros
- **Trocar stickers**: Adicionar arquivos PNG em `assets/stickers/`
- **Mudar spritesheet**: Substituir `assets/spritesheets/necromancer_64.png`

## ➕ Adicionando um Novo Filtro
1. Criar classe em `infrastructure/image_processing/`:
   ```python
   class MeuFiltro(ImageProcessorInterface):
       def process(self, image: Image) -> Image:
           # Implementar processamento
           return image
   ```
2. Registrar no `main.py`:
   ```python
   editor.register_processor('m', 'Meu Filtro', MeuFiltro())
   ```
3. Adicionar documentação em `EFEITOS_FILTROS.md`

## ❗ Solução de Problemas
| Problema | Causa Provável | Ação |
|----------|----------------|------|
| Webcam não abre | Permissões / webcam ocupada | Verificar se outro app está usando a câmera |
| Erro ao carregar imagem | Formato não suportado | Usar JPG, PNG ou BMP |
| Filtro não aplica | Tecla incorreta | Ver lista de teclas de atalho acima |
| Performance baixa | Processamento pesado | Reduzir resolução da imagem/vídeo |
| Stickers não aparecem | Arquivo não encontrado | Verificar se PNG está em `assets/stickers/` |
| Filtro de cachorro não funciona | Face não detectada | Melhorar iluminação, olhar para câmera |


## 📚 Referências

- [Documentação OpenCV](https://docs.opencv.org/4.x/)
- [Tutorial de Filtros](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html)
- [Operações Morfológicas](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
- Códigos base da professora (pasta HelloOpenCV)

---
