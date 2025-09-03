# UNISINOS – Lista de Exercícios 1 (Processamento Gráfico)

Introdução à OpenGL Moderna – Shaders & Buffers

Integrantes (se aplicável):
- Taimisson de Carvalho Schardosim

Como executar (CLion)
- Abra o projeto no CLion.
- Os alvos (targets) já estão configurados no CMake para cada exercício da pasta src/Lista1.
- No combo de Run/Debug, selecione o alvo desejado (Ex05a, Ex05b, …, Ex08) e rode.
- Alternativa: abra o painel CMake, escolha o target e clique em Build/Run.

Pré-requisitos do projeto
- CMake baixa GLFW e GLM automaticamente (FetchContent).
- GLAD já está no repositório: common/glad.c e include/glad/glad.h (CMake verifica isso).
- OpenGL: no Windows, linka com opengl32 automaticamente.

Arquivos/Targets desta lista
- Ex05a: dois triângulos – preenchido.
- Ex05b: dois triângulos – contorno.
- Ex05c: dois triângulos – pontos.
- Ex05d: dois triângulos – três formas juntas.
- Ex06: círculo por equação paramétrica.
- Ex06a: octógono.
- Ex06b: pentágono.
- Ex06c: pac-man.
- Ex06d: fatia de pizza.
- Ex06e: desafio – estrela.
- Ex07: espiral.
- Ex08: triângulo com cores por vértice (buffers e atributos mapeados no vertex shader).
Observação: HelloTriangle (referência) está em src/Lista2/HelloTriangle.cpp.

Como adicionar um novo exercício (ex.: Ex05b.cpp)
1) Crie o arquivo em src/Lista1/Ex05b.cpp.
2) Edite o CMakeLists.txt da raiz e acrescente Lista1/Ex05b na variável EXERCISES.
3) Salve: o CLion recarrega o CMake automaticamente. Se necessário, use Tools > CMake > Reset Cache and Reload Project ou o botão “Reload CMake Project”.
4) Selecione o target Ex05b e rode.
Dica: quando o CLion perguntar “Add to targets”, desmarque. A inclusão é controlada pelo CMake (já adicionamos via lista EXERCISES) e o GLAD é ligado automaticamente por ${GLAD_C_FILE}.

Enunciado resumido
0) Leitura obrigatória:
- https://learnopengl.com/#!Getting-started/Hello-Triangle
- https://learnopengl.com/#!Getting-started/Shaders
- http://antongerdelan.net/opengl/hellotriangle.html
Sugestões: Real-Time Rendering (cap. 2) e Computação Gráfica – Teoria e Prática (seção 5.1).
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

Dúvidas comuns
- “Arquivo glad.c não encontrado”: verifique common/glad.c e include/glad/glad.h. Estes caminhos já estão corretos no CMake (variável GLAD_C_FILE). Se removidos, baixe em https://glad.dav1d.de/ e recoloque nos mesmos diretórios.
- “Add to targets” ao criar arquivo: deixe desmarcado; gerenciamos pelo CMake.
- Recarregar CMake: Tools > CMake > Reset Cache and Reload Project, ou ícone de reload no painel CMake; alterações em CMakeLists normalmente disparam reload automático.

Referências
- LearnOpenGL (Hello Triangle e Shaders)
- Antón Gerdelan – Hello Triangle
- Real-Time Rendering (cap. 2) e Computação Gráfica – Teoria e Prática (seção 5.1)
