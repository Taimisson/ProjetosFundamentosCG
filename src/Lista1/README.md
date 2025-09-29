# UNISINOS – Lista de Exercícios 1 (Processamento Gráfico)

Introdução à OpenGL Moderna – Shaders & Buffers

**Integrante:**
- Taimisson de Carvalho Schardosim

## Como executar (CLion)
- Abra o projeto no CLion.
- Os alvos (targets) já estão configurados no CMake para cada exercício da pasta src/Lista1.
- No combo de Run/Debug, selecione o alvo desejado (L1_Ex05a, L1_Ex05b, …, L1_Ex09) e rode.
- Alternativa: abra o painel CMake, escolha o target e clique em Build/Run.

## Pré-requisitos do projeto
- CMake baixa GLFW e GLM automaticamente (FetchContent).
- GLAD já está no repositório: common/glad.c e include/glad/glad.h (CMake verifica isso).
- OpenGL: no Windows, linka com opengl32 automaticamente.

## Exercícios Implementados

### Exercícios 5 - Primitivas Básicas
- **L1_Ex05a**: Dois triângulos preenchidos (`GL_TRIANGLES`)
- **L1_Ex05b**: Dois triângulos em contorno (`GL_LINE_LOOP`)
- **L1_Ex05c**: Dois triângulos como pontos (`GL_POINTS`)
- **L1_Ex05d**: Combinação das três formas em uma única tela

### Exercícios 6 - Geometrias Complexas
- **L1_Ex06**: Círculo usando equação paramétrica
- **L1_Ex06a**: Octógono (8 lados)
- **L1_Ex06b**: Pentágono (5 lados)
- **L1_Ex06c**: Pac-man (círculo com "boca")
- **L1_Ex06d**: Fatia de pizza
- **L1_Ex06e**: Estrela (exercício desafio)

### Exercícios Avançados
- **L1_Ex07**: Espiral logarítmica
- **L1_Ex08**: Triângulo com cores por vértice e pontos circulares suavizados
- **L1_Ex09**: Casa quadriculada usando múltiplos VAOs e draw calls

**Observação:** HelloTriangle (referência) está em src/Lista2/HelloTriangle.cpp.

## Compilação

### Via CLion (Recomendado)
1. Abra o projeto no CLion
2. Selecione o target desejado (ex: L1_Ex05a)
3. Clique em Build/Run ou use Shift+F10

### Via linha de comando
```bash
cmake --build cmake-build-debug --target L1_Ex05a
cmake --build cmake-build-debug --target L1_Ex06
cmake --build cmake-build-debug --target L1_Ex08
```

## Como adicionar um novo exercício
1) Crie o arquivo em `src/Lista1/L1_ExXX.cpp`
2) Edite o `CMakeLists.txt` da raiz e acrescente `Lista1/L1_ExXX` na variável EXERCISES
3) Salve: o CLion recarrega o CMake automaticamente
4) Se necessário: Tools > CMake > Reset Cache and Reload Project
5) Selecione o target L1_ExXX e rode

**Dica:** Quando o CLion perguntar "Add to targets", desmarque. A inclusão é controlada pelo CMake.

## Conceitos Principais Abordados

### OpenGL Moderna
- **Shaders**: Vertex Shader e Fragment Shader obrigatórios
- **GLSL**: OpenGL Shading Language
- **Pipeline programável**: Controle das etapas de processamento

### Buffers e Objetos
- **VBO (Vertex Buffer Object)**: Armazena dados dos vértices na GPU
- **VAO (Vertex Array Object)**: Configura como interpretar os dados do VBO
- **EBO (Element Buffer Object)**: Índices para reutilizar vértices

### Primitivas Gráficas
- **GL_TRIANGLES**: Triângulos preenchidos
- **GL_LINE_LOOP**: Contornos fechados
- **GL_POINTS**: Pontos individuais

### Geometria Matemática
- **Equações paramétricas**: Para círculos e curvas
- **Coordenadas polares**: Conversão para cartesianas
- **Interpolação de cores**: Cores por vértice

## Enunciado e Leituras Obrigatórias

### Leituras Obrigatórias
- [LearnOpenGL - Hello Triangle](https://learnopengl.com/#!Getting-started/Hello-Triangle)
- [LearnOpenGL - Shaders](https://learnopengl.com/#!Getting-started/Shaders)
- [OpenGL Tutorial - Hello Triangle](http://antongerdelan.net/opengl/hellotriangle.html)

### Leituras Complementares
- Real-Time Rendering (cap. 2)
- Computação Gráfica – Teoria e Prática (seção 5.1)

### Questões Teóricas
1) O que é GLSL? Quais shaders obrigatórios no pipeline e o que processam?
2) O que são primitivas e como armazenar vértices na OpenGL?
3) Explique VBO, VAO e EBO, e a relação entre eles (pode ser um diagrama).
4) Analise HelloTriangle e localize shaders, VBOs e VAO.
5) Desenhe 2 triângulos: a) preenchido b) contorno c) pontos d) juntos.
6) Desenhe um círculo por parametrização. Depois: a) octógono b) pentágono c) pac-man d) fatia de pizza e) estrela (desafio).
7) Desenhe uma espiral.
8) Dado um triângulo P1/P2/P3 com cores RGB: a) buffers (VBO/VAO/EBO) b) atributos no vertex shader e implemente.
9) Reproduza um desenho quadriculado com primitivas (pode usar múltiplos VAOs e draw calls).
10) Implemente uma classe de shaders por arquivos (feito em aula, repositório atualizado).

## Respostas das Questões Teóricas

### 1. O que é a GLSL? Quais os dois tipos de shaders são obrigatórios no pipeline programável da versão atual que trabalhamos em aula e o que eles processam?

**GLSL (OpenGL Shading Language)** é uma linguagem de programação de alto nível baseada em C, desenvolvida especificamente para criar shaders que executam na GPU. É a linguagem padrão para programar o pipeline gráfico programável da OpenGL.

**Os dois shaders obrigatórios no pipeline programável são:**

1. **Vertex Shader**:
   - **Função**: Processa cada vértice individualmente
   - **Processamento**: 
     - Transformações de coordenadas (modelo → mundo → câmera → clip → tela)
     - Aplicação de matrizes de transformação (model, view, projection)
     - Cálculos de iluminação por vértice
     - Preparação de atributos para o fragment shader
   - **Entrada**: Atributos dos vértices (posição, cor, normais, coordenadas de textura)
   - **Saída**: `gl_Position` (posição final do vértice) e outros atributos interpolados

2. **Fragment Shader**:
   - **Função**: Processa cada pixel (fragment) individualmente
   - **Processamento**:
     - Determinação da cor final do pixel
     - Aplicação de texturas
     - Cálculos de iluminação por pixel
     - Efeitos de pós-processamento
   - **Entrada**: Atributos interpolados vindos do vertex shader
   - **Saída**: Cor final do fragment (`gl_FragColor` ou variável de saída customizada)

### 2. O que são primitivas gráficas? Como fazemos o armazenamento dos vértices na OpenGL?

**Primitivas Gráficas** são os elementos básicos de desenho que a GPU consegue renderizar diretamente. São formas geométricas fundamentais que servem como blocos de construção para objetos mais complexos.

**Principais tipos de primitivas na OpenGL:**
- **GL_POINTS**: Pontos individuais
- **GL_LINES**: Linhas entre pares de vértices
- **GL_LINE_STRIP**: Linhas conectadas sequencialmente
- **GL_LINE_LOOP**: Linhas conectadas em loop fechado
- **GL_TRIANGLES**: Triângulos independentes (mais comum)
- **GL_TRIANGLE_STRIP**: Triângulos conectados em tira
- **GL_TRIANGLE_FAN**: Triângulos em leque

**Armazenamento de vértices na OpenGL:**

1. **Na CPU (aplicação)**:
   ```cpp
   float vertices[] = {
       // posições      // cores
       -0.5f, -0.5f, 0.0f,  1.0f, 0.0f, 0.0f,  // vértice 0
        0.5f, -0.5f, 0.0f,  0.0f, 1.0f, 0.0f,  // vértice 1
        0.0f,  0.5f, 0.0f,  0.0f, 0.0f, 1.0f   // vértice 2
   };
   ```

2. **Na GPU (VBO - Vertex Buffer Object)**:
   ```cpp
   GLuint VBO;
   glGenBuffers(1, &VBO);
   glBindBuffer(GL_ARRAY_BUFFER, VBO);
   glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
   ```

### 3. Explique o que é VBO, VAO e EBO, e como se relacionam

**VBO (Vertex Buffer Object)**:
- **Definição**: Buffer que armazena dados dos vértices na memória da GPU
- **Função**: Transfere grandes quantidades de dados de vértices da CPU para GPU de uma só vez
- **Conteúdo**: Posições, cores, normais, coordenadas de textura, etc.
- **Vantagem**: Acesso muito mais rápido que transferir dados a cada frame

**VAO (Vertex Array Object)**:
- **Definição**: Objeto que armazena configurações de como interpretar os dados dos VBOs
- **Função**: "Lembra" como os atributos dos vértices estão organizados
- **Conteúdo**: Ponteiros para VBOs, layout dos atributos, habilitação de atributos
- **Vantagem**: Permite trocar entre diferentes configurações de vértices rapidamente

**EBO (Element Buffer Object) / IBO (Index Buffer Object)**:
- **Definição**: Buffer que armazena índices dos vértices para reutilização
- **Função**: Evita duplicação de vértices compartilhados entre primitivas
- **Exemplo**: Para um quadrado, ao invés de 6 vértices (2 triângulos), usa 4 vértices + 6 índices
- **Vantagem**: Economiza memória e largura de banda

**Relação entre VBO, VAO e EBO:**

```
VAO (contém configurações)
├── VBO #1 (posições dos vértices)
├── VBO #2 (cores dos vértices)  
├── VBO #3 (coordenadas de textura)
└── EBO (índices para reutilizar vértices)
```

**Fluxo de uso:**
1. **Criar VAO**: `glGenVertexArrays()` e `glBindVertexArray()`
2. **Criar e preencher VBO**: `glGenBuffers()`, `glBindBuffer()`, `glBufferData()`
3. **Configurar atributos**: `glVertexAttribPointer()`, `glEnableVertexAttribArray()`
4. **Opcional - Criar EBO**: Para reutilizar vértices
5. **Renderizar**: `glBindVertexArray()` + `glDrawArrays()` ou `glDrawElements()`

### 4. Análise do código fonte do projeto Hello Triangle

**No HelloTriangle.cpp, os conceitos estão organizados da seguinte forma:**

**Shaders:**
```cpp
// Vertex Shader - processa cada vértice
const GLchar *vertexShaderSource = R"(
 #version 400
 layout (location = 0) in vec3 position;
 void main() {
     gl_Position = vec4(position.x, position.y, position.z, 1.0);
 })";

// Fragment Shader - processa cada pixel
const GLchar *fragmentShaderSource = R"(
 #version 400
 uniform vec4 inputColor;
 out vec4 color;
 void main() {
     color = inputColor;
 })";
```

**VBO (na função setupGeometry()):**
```cpp
// Dados dos vértices na CPU
float vertices[] = { /* coordenadas dos vértices */ };

// Criação e preenchimento do VBO na GPU
GLuint VBO;
glGenBuffers(1, &VBO);
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
```

**VAO (na função setupGeometry()):**
```cpp
// Criação do VAO
GLuint VAO;
glGenVertexArrays(1, &VAO);
glBindVertexArray(VAO);

// Configuração dos atributos dos vértices
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);
```

**Renderização (no loop principal):**
```cpp
// Ativação do programa de shader
glUseProgram(shaderProgram);

// Binding do VAO (que "lembra" toda configuração)
glBindVertexArray(VAO);

// Desenho das primitivas
glDrawArrays(GL_TRIANGLES, 0, 3);
```

**Relação entre os conceitos:**
1. **Shaders** definem COMO processar os dados
2. **VBO** armazena OS DADOS dos vértices na GPU
3. **VAO** configura COMO INTERPRETAR os dados do VBO
4. **Pipeline**: VAO → Vertex Shader → Rasterização → Fragment Shader → Tela
