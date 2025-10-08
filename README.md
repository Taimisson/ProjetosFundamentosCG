# Projeto de Exercícios de Processamento Gráfico

Repositório para os exercícios da disciplina **Processamento Gráfico / Fundamentos de Computação Gráfica** utilizando **OpenGL moderno (Core Profile)** em C++.

> **📝 Nota:** As respostas às questões teóricas de cada lista estão documentadas nos arquivos README dentro de cada pasta (`src/Lista1/README.md`, `src/Lista2/README.md`, etc.).

## 👥 Integrantes do Grupo
Preencha com os nomes do(s) autor(es):
Taimisson de Carvalho Schardosim

## 🎯 Objetivo
Centralizar, compilar e executar os exercícios práticos (listas) envolvendo pipeline programável (Vertex/Fragment Shaders), criação de janelas, desenho de primitivas e uso de bibliotecas auxiliares para desenvolvimento gráfico.

## 🏗️ Tecnologias & Dependências
As bibliotecas externas são baixadas automaticamente via **CMake FetchContent**:
- **GLFW** (janela, contexto OpenGL, input)
- **GLAD** (carregador de funções OpenGL) – arquivo `common/glad.c`
- **GLM** (matemática para gráficos)
- **stb_image** (carregamento de texturas – ainda não usado, mas preparado)

Requisitos mínimos recomendados:
- CMake >= 3.11
- Compilador C++ com suporte a C++17 (g++ 9+, clang 9+, MSVC 2019+)
- Driver/GPU com suporte a OpenGL 4.0 (ajustável se necessário)

## 📂 Estrutura Principal
```
common/        -> glad.c e utilitários
include/       -> headers (glad.h, etc.)
src/Lista1/    -> Exercícios da Lista 1
src/Lista2/    -> Exercícios da Lista 2
CMakeLists.txt -> Configuração de build (gera um executável por exercício)
```
Cada novo exercício inserido em `src/ListaX/Nome.cpp` deve ser adicionado à lista `EXERCISES` no `CMakeLists.txt`.

## 🔧 Compilação
### Opção 1: Terminal (genérico)
```bash
# Na raiz do repositório
mkdir -p build
cd build
cmake ..
cmake --build . --config Debug
```
Os executáveis serão gerados dentro de `build/` (ou em subpastas conforme o gerador).

### Opção 2: CLion
- Abrir a pasta do projeto.
- CLion detecta o CMake automaticamente.
- Escolher o alvo (por exemplo, `HelloTriangle`) e rodar.

### Opção 3: VS Code
- Instalar extensões: C/C++, CMake Tools.
- Abrir a pasta do projeto.
- Command Palette: `CMake: Configure` e depois `CMake: Build`.
- Selecionar o target desejado.

## ▶️ Execução
Após compilar:
- Linux/macOS: `./HelloTriangle` ou `./Ex5`
- Windows (PowerShell/CMD dentro de build): `./HelloTriangle.exe` ou `./Ex5.exe`

A janela deve exibir:
- FPS atualizado (no caso de `Ex5`).
- Um triângulo azul (ou dois formando figura) renderizado via shaders simples.

## 🎮 Controles
| Tecla | Ação |
|-------|------|
| ESC   | Fecha a janela / encerra o loop principal |

## 🛠️ Customizações Rápidas
- Alterar resolução: modificar constantes `WIDTH` e `HEIGHT` no arquivo do exercício.
- Alterar cor: editar a chamada `glUniform4f(colorLoc, ...)` ou o fragment shader.
- Ajustar versão OpenGL: comentar ou modificar `glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, ...)` e `MINOR` se houver incompatibilidade.

## ➕ Adicionando um Novo Exercício
1. Criar arquivo: `src/ListaN/MeuEx.cpp`.
2. Copiar um template básico (por exemplo, de `HelloTriangle.cpp`).
3. Adicionar o caminho (sem `.cpp`) em `EXERCISES` dentro do `CMakeLists.txt`:
   ```cmake
   set(EXERCISES
       Lista2/HelloTriangle
       Lista1/Ex5
       Lista3/MeuEx
   )
   ```
4. Reconfigurar o CMake (rodar `cmake ..` novamente) e compilar.

## ❗ Solução de Problemas
| Problema | Causa Provável | Ação |
|----------|----------------|------|
| Janela não abre / crash | Versão OpenGL não suportada | Comentar hints de versão ou reduzir para 3.3 |
| Erro GLAD / símbolo indefinido | `glad.c` não incluido | Confirmar que `common/glad.c` está no alvo (já está no loop do CMake) |
| Tela preta | Geometria não enviada / shader falhou | Verificar logs de compilação de shader no terminal |
| Build falha no Windows | Falta de toolchain | Instalar MSVC Build Tools ou Mingw-w64 |
| FPS muito baixo | Driver/software rasterizer | Atualizar driver GPU / usar GPU dedicada |

---
