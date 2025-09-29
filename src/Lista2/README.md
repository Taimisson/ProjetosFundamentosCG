# Lista de Exercícios 2 - Processamento Gráfico
## Transformações e Viewport

### Descrição
Esta lista aborda conceitos fundamentais de transformações de coordenadas, matrizes de projeção ortográfica e controle de viewport em OpenGL.

### Exercícios Implementados

#### Ex01.cpp - Modificação da Janela do Mundo
**Objetivo:** Modificar a janela do mundo (window/ortho) para os limites: xmin=-10, xmax=10, ymin=-10, ymax=10.

**Implementação:**
- Utiliza `glm::ortho(-10.0f, 10.0f, -10.0f, 10.0f, -1.0f, 1.0f)`
- Desenha dois triângulos coloridos em um espaço de coordenadas maior
- Demonstra como alterar o sistema de coordenadas do mundo

**Conceitos:** Matriz de projeção ortográfica, sistemas de coordenadas

#### Ex02.cpp - Sistema de Coordenadas de Tela
**Objetivo:** Modificar a janela do mundo para: xmin=0, xmax=800, ymin=600, ymax=0.

**Implementação:**
- Utiliza `glm::ortho(0.0f, 800.0f, 600.0f, 0.0f, -1.0f, 1.0f)`
- Sistema de coordenadas similar ao de uma tela (origem no canto superior esquerdo)
- Y invertido (ymin=600, ymax=0)
- Triângulos posicionados usando coordenadas de pixel

**Conceitos:** Sistema de coordenadas de tela, inversão de eixo Y

#### Ex03.cpp - Desenho com Câmera 2D
**Objetivo:** Utilizando a câmera 2D do exercício anterior, desenhe algo na tela. O que acontece quando posicionamos os objetos? Por que é útil essa configuração?

**Implementação:**
- Usa o mesmo sistema de coordenadas do Ex02 (coordenadas de tela)
- Desenha uma casa simples composta por: base, telhado, porta e janela
- Cada elemento é posicionado com coordenadas exatas em pixels
- Demonstra a precisão do posicionamento em coordenadas de tela

**Por que é útil?**
- **Posicionamento preciso**: Facilita colocar elementos em posições exatas
- **Interface gráfica**: Ideal para botões, menus, HUDs
- **Correspondência 1:1**: 1 unidade = 1 pixel na tela
- **Facilita cálculos**: Dimensões em pixels são intuitivas

**Conceitos:** Coordenadas de pixel, design de interfaces, posicionamento preciso

#### Ex04.cpp - Controle de Viewport
**Objetivo:** Modificar o viewport para desenhar a cena apenas em um quadrante específico da janela.

**Implementação:**
- Utiliza `glViewport(400, 300, 400, 300)` para renderizar apenas no quadrante inferior direito
- Mantém a geometria original mas restringe a área de renderização
- Demonstra a diferença entre sistema de coordenadas do mundo e viewport

**Conceitos:** Viewport, área de renderização, mapeamento de coordenadas

### Compilação e Execução

Para compilar os exercícios, certifique-se de que o CMakeLists.txt está atualizado e execute no CLion:

1. **Através do CLion:**
   - Build → Build Project (Ctrl+F9)
   - Ou clique em "Build" para targets específicos

2. **Via linha de comando (se necessário):**
   ```bash
   cmake --build cmake-build-debug --target Ex01
   cmake --build cmake-build-debug --target Ex02
   cmake --build cmake-debug --target Ex03
   cmake --build cmake-build-debug --target Ex04
   ```

### Conceitos Principais Abordados

1. **Matriz de Projeção Ortográfica**: Define como as coordenadas 3D são mapeadas para a tela 2D
2. **Sistema de Coordenadas**: Diferentes sistemas (mundo, tela, normalizado)
3. **Viewport**: Controla qual região da janela será usada para renderização
4. **Transformações de Coordenadas**: Como converter entre diferentes sistemas

### Observações Importantes

- **Ex01**: Amplia o espaço de coordenadas, permitindo objetos maiores
- **Ex02**: Simula coordenadas de tela (útil para interfaces gráficas)  
- **Ex03**: Demonstra o uso prático de coordenadas de tela para desenho preciso
- **Ex04**: Demonstra renderização em sub-regiões da janela

### Análise dos Resultados

#### Ex03 - Por que coordenadas de tela são úteis?

1. **Precisão**: Você especifica exatamente onde cada pixel será desenhado
2. **Intuitividade**: As coordenadas correspondem diretamente à posição na tela
3. **Facilita UI**: Botões, menus e elementos de interface ficam mais fáceis de posicionar
4. **Compatibilidade**: Funciona bem com ferramentas de design gráfico

### Para Estudar Mais

- Matriz de projeção ortográfica vs perspectiva
- Transformações de viewport
- Pipeline de transformações gráficas
- Sistemas de coordenadas homogêneas
- Design de interfaces gráficas com OpenGL
