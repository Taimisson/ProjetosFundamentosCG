# UNISINOS – Lista de Exercícios 2 (Processamento Gráfico)

Transformações e Viewport

**Integrante:**
- Taimisson de Carvalho Schardosim

## Como executar (CLion)
- Abra o projeto no CLion.
- Os alvos (targets) já estão configurados no CMake para cada exercício da pasta src/Lista2.
- No combo de Run/Debug, selecione o alvo desejado (L2_Ex01, L2_Ex02, L2_Ex04, L2_Ex05, L2_Ex06) e rode.
- Alternativa: abra o painel CMake, escolha o target e clique em Build/Run.

## Pré-requisitos do projeto
- CMake baixa GLFW e GLM automaticamente (FetchContent).
- GLAD já está no repositório: common/glad.c e include/glad/glad.h (CMake verifica isso).
- OpenGL: no Windows, linka com opengl32 automaticamente.

## Exercícios Implementados

### Exercícios de Sistemas de Coordenadas
- **L2_Ex01**: Janela do mundo expandida (-10 a 10) - Coordenadas de mundo ampliadas
- **L2_Ex02**: Sistema de coordenadas de tela (0-800, 600-0) - Coordenadas de pixel

### Exercícios de Viewport
- **L2_Ex04**: Controle de viewport - Renderização em quadrante específico
- **L2_Ex05**: Múltiplos viewports - Mesma cena em 4 quadrantes

### Exercícios Interativos
- **L2_Ex06**: Criação interativa de triângulos com mouse - Geometria dinâmica

### Arquivos de Referência
- **HelloTriangle**: Exemplo básico de triângulo OpenGL moderna
- **HelloOrtho**: Demonstração de projeções ortográficas
- **HelloTransforms**: Transformações básicas com GLM
- **HelloTransformsHardCoded**: Transformações manuais sem GLM
- **HelloTexture**: Aplicação básica de texturas
- **HelloSprites**: Sistema de sprites 2D
- **Sprite.cpp/h**: Classe para gerenciamento de sprites

## Compilação

### Via CLion (Recomendado)
1. Abra o projeto no CLion
2. Selecione o target desejado (ex: L2_Ex01)
3. Clique em Build/Run ou use Shift+F10

### Via linha de comando
```bash
cmake --build cmake-build-debug --target L2_Ex01
cmake --build cmake-build-debug --target L2_Ex02
cmake --build cmake-build-debug --target L2_Ex04
cmake --build cmake-build-debug --target L2_Ex05
cmake --build cmake-build-debug --target L2_Ex06
```

## Como adicionar um novo exercício
1) Crie o arquivo em `src/Lista2/L2_ExXX.cpp`
2) Edite o `CMakeLists.txt` da raiz e acrescente `Lista2/L2_ExXX` na variável EXERCISES
3) Salve: o CLion recarrega o CMake automaticamente
4) Se necessário: Tools > CMake > Reset Cache and Reload Project
5) Selecione o target L2_ExXX e rode

**Dica:** Quando o CLion perguntar "Add to targets", desmarque. A inclusão é controlada pelo CMake.

## Conceitos Principais Abordados

### Sistemas de Coordenadas
- **Coordenadas de mundo**: Sistema expandido para objetos maiores
- **Coordenadas de tela**: Sistema pixel-perfeito para interfaces
- **Coordenadas normalizadas**: Sistema padrão OpenGL (-1 a 1)

### Matrizes de Projeção
- **Projeção ortográfica**: Mapeamento 3D → 2D sem perspectiva
- **glm::ortho()**: Função para criar matrizes de projeção
- **Transformações de coordenadas**: Conversão entre sistemas

### Viewport e Renderização
- **Viewport**: Controle da região de renderização na janela
- **Multiple viewports**: Divisão da tela em múltiplas regiões
- **Mapeamento de coordenadas**: Mundo → Tela via viewport

### Interatividade
- **Input do mouse**: Captura de cliques e posições
- **Geometria dinâmica**: Criação de objetos em tempo real
- **Feedback visual**: Resposta imediata às ações do usuário

## Detalhamento dos Exercícios

### L2_Ex01 - Modificação da Janela do Mundo
**Objetivo:** Modificar a janela do mundo para os limites: xmin=-10, xmax=10, ymin=-10, ymax=10.

**Implementação:**
- Utiliza `glm::ortho(-10.0f, 10.0f, -10.0f, 10.0f, -1.0f, 1.0f)`
- Desenha dois triângulos coloridos em um espaço de coordenadas maior
- Demonstra como alterar o sistema de coordenadas do mundo

**Conceitos:** Matriz de projeção ortográfica, sistemas de coordenadas

### L2_Ex02 - Sistema de Coordenadas de Tela
**Objetivo:** Modificar a janela do mundo para: xmin=0, xmax=800, ymin=600, ymax=0.

**Implementação:**
- Utiliza `glm::ortho(0.0f, 800.0f, 600.0f, 0.0f, -1.0f, 1.0f)`
- Sistema de coordenadas similar ao de uma tela (origem no canto superior esquerdo)
- Y invertido (ymin=600, ymax=0)
- Triângulos posicionados usando coordenadas de pixel

**Conceitos:** Sistema de coordenadas de tela, inversão de eixo Y

### L2_Ex04 - Controle de Viewport
**Objetivo:** Modificar o viewport para desenhar a cena apenas em um quadrante específico da janela.

**Implementação:**
- Utiliza `glViewport(400, 300, 400, 300)` para renderizar apenas no quadrante inferior direito
- Mantém a geometria original mas restringe a área de renderização
- Demonstra a diferença entre sistema de coordenadas do mundo e viewport

**Conceitos:** Viewport, área de renderização, mapeamento de coordenadas

### L2_Ex05 - Múltiplos Viewports
**Objetivo:** Desenhar a mesma cena nos 4 quadrantes da janela.

**Implementação:**
- Renderiza a mesma geometria em 4 viewports diferentes
- Cada quadrante representa uma região da janela (superior esquerdo, superior direito, etc.)
- Demonstra reutilização de geometria com diferentes áreas de renderização
- Inclui contornos para destacar as diferentes regiões

**Conceitos:** Múltiplos viewports, reutilização de geometria, divisão de tela

### L2_Ex06 - Criação Interativa de Triângulos
**Objetivo:** Criar triângulos clicando na tela com o mouse.

**Implementação:**
- Sistema de input do mouse para capturar cliques
- A cada 3 cliques, um novo triângulo é formado
- Cores aleatórias para cada triângulo
- Visualização de vértices temporários como pontos
- Contador de triângulos no título da janela
- Sistema de coordenadas de tela para posicionamento preciso

**Conceitos:** Interatividade, input do mouse, criação dinâmica de geometria, coordenadas de tela

## Análise dos Resultados

### Por que coordenadas de tela são úteis?

1. **Precisão**: Você especifica exatamente onde cada pixel será desenhado
2. **Intuitividade**: As coordenadas correspondem diretamente à posição na tela
3. **Facilita UI**: Botões, menus e elementos de interface ficam mais fáceis de posicionar
4. **Compatibilidade**: Funciona bem com ferramentas de design gráfico
5. **Desenvolvimento de jogos**: Ideal para HUDs, menus e elementos de interface

### Aplicações Práticas

- **L2_Ex01**: Simulações científicas, jogos com mundo expandido
- **L2_Ex02/L2_Ex06**: Design de interfaces gráficas, editores
- **L2_Ex04/L2_Ex05**: Aplicações multi-janela, dashboards, ferramentas de análise
- **L2_Ex06**: Editores gráficos, ferramentas de desenho, CAD simplificado

### Observações Importantes

- **L2_Ex01**: Amplia o espaço de coordenadas, permitindo objetos maiores
- **L2_Ex02**: Simula coordenadas de tela (útil para interfaces gráficas)
- **L2_Ex04**: Demonstra renderização em sub-regiões da janela
- **L2_Ex05**: Mostra como reutilizar geometria em múltiplas regiões
- **L2_Ex06**: Combina interatividade com coordenadas de tela para criação dinâmica
