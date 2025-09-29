/*
 * L2_Ex06 - Exercício 6 da Lista 2
 * Criar triângulos a partir do clique do mouse
 *
 * Adaptado por: Rossana Baptista Queiroz
 *
 * Disciplinas:
 *   - Processamento Gráfico (Ciência da Computação - Híbrido)
 *   - Processamento Gráfico: Fundamentos (Ciência da Computação - Presencial)
 *   - Fundamentos de Computação Gráfica (Jogos Digitais)
 *
 * Descrição:
 *   Este exercício permite criar triângulos clicando na tela. A cada 3 cliques,
 *   um novo triângulo é criado com uma cor aleatória.
 *
 * Histórico:
 *   - Versão inicial: 07/04/2017
 *   - Última atualização: 18/03/2025
 *
 */

#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <ctime>

using namespace std;

// GLAD
#include <glad/glad.h>

// GLFW
#include <GLFW/glfw3.h>

// GLM
#include <glm/glm.hpp> 
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

using namespace glm;

// Estrutura para armazenar vértices
struct Vertex {
    float x, y, z;
    float r, g, b;
};

// Variáveis globais
vector<Vertex> vertices;
vector<Vertex> currentTriangle;
GLuint VAO, VBO;
int triangleCount = 0;

// Protótipos das funções
void key_callback(GLFWwindow *window, int key, int scancode, int action, int mode);
void mouse_button_callback(GLFWwindow* window, int button, int action, int mods);
int setupShader();
void updateGeometry();
vec3 generateRandomColor();

// Dimensões da janela
const GLuint WIDTH = 800, HEIGHT = 600;

// Código fonte do Vertex Shader (em GLSL)
const GLchar *vertexShaderSource = R"(
 #version 400
 layout (location = 0) in vec3 position;
 layout (location = 1) in vec3 color;
 out vec3 vColor; 
 uniform mat4 projection;
 void main()
 {
	 gl_Position = projection * vec4(position.x, position.y, position.z, 1.0);
	 vColor = color;
 }
 )";

// Código fonte do Fragment Shader (em GLSL)
const GLchar *fragmentShaderSource = R"(
 #version 400
 in vec3 vColor;
 out vec4 color;
 void main()
 {
	 color = vec4(vColor,1.0);
 }
 )";

// Função MAIN
int main()
{
	// Inicialização da GLFW
	glfwInit();

	// Inicializa gerador de números aleatórios
	srand(time(nullptr));

	// Criação da janela GLFW
	GLFWwindow *window = glfwCreateWindow(WIDTH, HEIGHT, "L2_Ex06 - Criar Triângulos com Mouse -- Taimisson", nullptr, nullptr);
	if (!window)
	{
		std::cerr << "Falha ao criar a janela GLFW" << std::endl;
		glfwTerminate();
		return -1;
	}
	glfwMakeContextCurrent(window);

	// Registrando callbacks
	glfwSetKeyCallback(window, key_callback);
	glfwSetMouseButtonCallback(window, mouse_button_callback);

	// GLAD: carrega todos os ponteiros de funções da OpenGL
	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
	{
		std::cerr << "Falha ao inicializar GLAD" << std::endl;
		return -1;
	}

	// Obtendo as informações de versão
	const GLubyte *renderer = glGetString(GL_RENDERER);
	const GLubyte *version = glGetString(GL_VERSION);
	cout << "Renderer: " << renderer << endl;
	cout << "OpenGL version supported " << version << endl;

	// Compilando e buildando o programa de shader
	GLuint shaderID = setupShader();

	// Configuração inicial do VAO e VBO
	glGenVertexArrays(1, &VAO);
	glGenBuffers(1, &VBO);

	glUseProgram(shaderID);

	double prev_s = glfwGetTime();
	double title_countdown_s = 0.1;

	// Criação da matriz de projeção - coordenadas de tela (0,800,600,0)
	mat4 projection = ortho(0.0f, (float)WIDTH, (float)HEIGHT, 0.0f, -1.0f, 1.0f);

	// Mandar a matriz de projeção para o shader
	glUniformMatrix4fv(glGetUniformLocation(shaderID, "projection"), 1, GL_FALSE, value_ptr(projection));

	cout << "Clique na tela para criar vértices. A cada 3 cliques, um triângulo será criado!" << endl;
	cout << "Pressione ESC para sair." << endl;

	// Loop da aplicação - "game loop"
	while (!glfwWindowShouldClose(window))
	{
		// Calcula e mostra o FPS na barra de título
		{
			double curr_s = glfwGetTime();
			double elapsed_s = curr_s - prev_s;
			prev_s = curr_s;

			title_countdown_s -= elapsed_s;
			if (title_countdown_s <= 0.0 && elapsed_s > 0.0)
			{
				double fps = 1.0 / elapsed_s;
				char tmp[256];
				sprintf(tmp, "L2_Ex06 - Triângulos: %d, Vértices: %d/3 -- FPS %.2lf",
					triangleCount, (int)currentTriangle.size(), fps);
				glfwSetWindowTitle(window, tmp);
				title_countdown_s = 0.1;
			}
		}

		// Checa eventos de input
		glfwPollEvents();

		// Limpa o buffer de cor
		glClearColor(0.2f, 0.2f, 0.2f, 1.0f); // Fundo cinza escuro
		glClear(GL_COLOR_BUFFER_BIT);

		// Viewport para tela inteira
		glViewport(0, 0, WIDTH, HEIGHT);

		// Desenha todos os triângulos criados
		if (!vertices.empty())
		{
			glBindVertexArray(VAO);
			glDrawArrays(GL_TRIANGLES, 0, vertices.size());
			glBindVertexArray(0);
		}

		// Desenha os vértices do triângulo atual sendo criado como pontos
		if (!currentTriangle.empty())
		{
			glPointSize(8.0f);

			// Cria um VAO temporário para os pontos
			GLuint tempVAO, tempVBO;
			glGenVertexArrays(1, &tempVAO);
			glGenBuffers(1, &tempVBO);

			glBindVertexArray(tempVAO);
			glBindBuffer(GL_ARRAY_BUFFER, tempVBO);
			glBufferData(GL_ARRAY_BUFFER, currentTriangle.size() * sizeof(Vertex), currentTriangle.data(), GL_DYNAMIC_DRAW);

			glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), (void*)0);
			glEnableVertexAttribArray(0);
			glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), (void*)(3 * sizeof(float)));
			glEnableVertexAttribArray(1);

			glDrawArrays(GL_POINTS, 0, currentTriangle.size());

			// Limpa VAO temporário
			glDeleteVertexArrays(1, &tempVAO);
			glDeleteBuffers(1, &tempVBO);
		}

		// Troca os buffers da tela
		glfwSwapBuffers(window);
	}

	// Limpeza
	glDeleteVertexArrays(1, &VAO);
	glDeleteBuffers(1, &VBO);
	glfwTerminate();
	return 0;
}

// Função de callback de teclado
void key_callback(GLFWwindow *window, int key, int scancode, int action, int mode)
{
	if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
		glfwSetWindowShouldClose(window, GL_TRUE);
}

// Função de callback do mouse
void mouse_button_callback(GLFWwindow* window, int button, int action, int mods)
{
	if (button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_PRESS)
	{
		double xpos, ypos;
		glfwGetCursorPos(window, &xpos, &ypos);

		// Converte coordenadas da tela para coordenadas do mundo
		float worldX = (float)xpos;
		float worldY = (float)ypos;

		// Gera cor para este vértice (será a cor do triângulo quando completado)
		static vec3 currentColor = generateRandomColor();

		// Cria o vértice
		Vertex vertex;
		vertex.x = worldX;
		vertex.y = worldY;
		vertex.z = 0.0f;
		vertex.r = currentColor.r;
		vertex.g = currentColor.g;
		vertex.b = currentColor.b;

		// Adiciona o vértice ao triângulo atual
		currentTriangle.push_back(vertex);

		cout << "Vértice " << currentTriangle.size() << " criado em (" << worldX << ", " << worldY << ")" << endl;

		// Se completou um triângulo (3 vértices)
		if (currentTriangle.size() == 3)
		{
			// Adiciona os 3 vértices aos triângulos finalizados
			for (const auto& v : currentTriangle)
			{
				vertices.push_back(v);
			}

			triangleCount++;
			cout << "Triângulo " << triangleCount << " criado!" << endl;

			// Atualiza a geometria no OpenGL
			updateGeometry();

			// Limpa o triângulo atual e gera nova cor para o próximo
			currentTriangle.clear();
			currentColor = generateRandomColor();
		}
	}
}

// Função para configurar os shaders
int setupShader()
{
	// Vertex shader
	GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
	glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
	glCompileShader(vertexShader);

	GLint success;
	GLchar infoLog[512];
	glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
	if (!success)
	{
		glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
	}

	// Fragment shader
	GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
	glCompileShader(fragmentShader);

	glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
	if (!success)
	{
		glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" << infoLog << std::endl;
	}

	// Linkando os shaders
	GLuint shaderProgram = glCreateProgram();
	glAttachShader(shaderProgram, vertexShader);
	glAttachShader(shaderProgram, fragmentShader);
	glLinkProgram(shaderProgram);

	glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
	if (!success)
	{
		glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n" << infoLog << std::endl;
	}

	glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);

	return shaderProgram;
}

// Atualiza a geometria no OpenGL
void updateGeometry()
{
	if (vertices.empty()) return;

	glBindVertexArray(VAO);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);

	// Envia todos os vértices para o buffer
	glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(Vertex), vertices.data(), GL_DYNAMIC_DRAW);

	// Configura os atributos dos vértices
	// Posição (x, y, z)
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), (void*)0);
	glEnableVertexAttribArray(0);

	// Cor (r, g, b)
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);

	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindVertexArray(0);
}

// Gera uma cor aleatória
vec3 generateRandomColor()
{
	return vec3(
		(rand() % 256) / 255.0f,  // R
		(rand() % 256) / 255.0f,  // G
		(rand() % 256) / 255.0f   // B
	);
}

