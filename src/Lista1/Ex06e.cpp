#include <iostream>
#include <string>
#include <assert.h>
#include <cmath>

using namespace std;

#include <glad/glad.h>

#include <GLFW/glfw3.h>
#include <GLFW/glfw3.h>

void key_callback(GLFWwindow *window, int key, int scancode, int action, int mode);

int setupShader();
int setupGeometry();

const GLuint WIDTH = 800, HEIGHT = 800;

const int segments = 5;

const GLchar *vertexShaderSource = R"(
 #version 400
 layout (location = 0) in vec3 position;
 void main()
 {
	 gl_Position = vec4(position.x, position.y, position.z, 1.0);
 }
 )";

const GLchar *fragmentShaderSource = R"(
 #version 400
 uniform vec4 inputColor;
 out vec4 color;
 void main()
 {
	 color = inputColor;
 }
 )";

int main()
{
	glfwInit();

	 glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
	 glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);
	 glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
	 glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	GLFWwindow *window = glfwCreateWindow(WIDTH, HEIGHT, "Ola Triangulo! -- Rossana", nullptr, nullptr);
	if (!window)
	{
		std::cerr << "Falha ao criar a janela GLFW" << std::endl;
		glfwTerminate();
		return -1;
	}
	glfwMakeContextCurrent(window);

	glfwSetKeyCallback(window, key_callback);

	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
	{
		std::cerr << "Falha ao inicializar GLAD" << std::endl;
		return -1;
	}

	const GLubyte *renderer = glGetString(GL_RENDERER); /* get renderer string */
	const GLubyte *version = glGetString(GL_VERSION);	/* version as a string */
	cout << "Renderer: " << renderer << endl;
	cout << "OpenGL version supported " << version << endl;

	int width, height;
	glfwGetFramebufferSize(window, &width, &height);
	glViewport(0, 0, width, height);

	GLuint shaderID = setupShader();

	GLuint VAO = setupGeometry();

	GLint colorLoc = glGetUniformLocation(shaderID, "inputColor");

	glUseProgram(shaderID); // Reseta o estado do shader para evitar problemas futuros

	while (!glfwWindowShouldClose(window))
	{
		glfwPollEvents();

		glClearColor(0.0f, 0.0f, 0.0f, 1.0f); // cor de fundo
		glClear(GL_COLOR_BUFFER_BIT);

		glLineWidth(10);
		glPointSize(20);

		glBindVertexArray(VAO); // Conectando ao buffer de geometria

		glUniform4f(colorLoc, 0.0f, 1.0f, 1.0f, 1.0f); // Azul ciano (cyan))

		glDrawArrays(GL_TRIANGLES, 0, segments * 3 * 2);

		// glBindVertexArray(0); // Desnecessário aqui, pois não há múltiplos VAOs

		glfwSwapBuffers(window);
	}
	glDeleteVertexArrays(1, &VAO);
	glfwTerminate();
	return 0;
}

void key_callback(GLFWwindow *window, int key, int scancode, int action, int mode)
{
	if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
		glfwSetWindowShouldClose(window, GL_TRUE);
}

int setupShader()
{
	GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
	glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
	glCompileShader(vertexShader);
	GLint success;
	GLchar infoLog[512];
	glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
	if (!success)
	{
		glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n"
				  << infoLog << std::endl;
	}
	GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
	glCompileShader(fragmentShader);
	glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
	if (!success)
	{
		glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n"
				  << infoLog << std::endl;
	}
	GLuint shaderProgram = glCreateProgram();
	glAttachShader(shaderProgram, vertexShader);
	glAttachShader(shaderProgram, fragmentShader);
	glLinkProgram(shaderProgram);
	glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
	if (!success)
	{
		glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n"
				  << infoLog << std::endl;
	}
	glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);

	return shaderProgram;
}

int setupGeometry()
{
	float centerX = 0.0f;
	float centerY = 0.0f;
	float radius = 0.5f;
	float radius2 = 0.18f;
	GLfloat vertices[segments * 9 * 2];

	for (int i = 0; i < segments; ++i) {
		float theta1 = 4.08 + 2.0f * M_PI * i / segments;
		float theta2 = 4.08 + 2.0f * M_PI * (i + 1) / segments;

		vertices[i*18] = centerX;
		vertices[i*18+1] = centerY;
		vertices[i*18+2] = 0.0f;

		vertices[i*18+3] = centerX + radius2 * cos(theta1);
		vertices[i*18+4] = centerY + radius2 * sin(theta1);
		vertices[i*18+5] = 0.0f;

		vertices[i*18+6] = centerX + radius * cos(theta2);
		vertices[i*18+7] = centerY + radius * sin(theta2);
		vertices[i*18+8] = 0.0f;

		vertices[i*18+9] = centerX;
		vertices[i*18+10] = centerY;
		vertices[i*18+11] = 0.0f;

		vertices[i*18+12] = centerX + radius * cos(theta1);
		vertices[i*18+13] = centerY + radius * sin(theta1);
		vertices[i*18+14] = 0.0f;

		vertices[i*18+15] = centerX + radius2 * cos(theta2);
		vertices[i*18+16] = centerY + radius2 * sin(theta2);
		vertices[i*18+17] = 0.0f;
	}

	GLuint VBO, VAO;
	// Geração do identificador do VBO
	glGenBuffers(1, &VBO);
	// Faz a conexão (vincula) do buffer como um buffer de array
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	// Envia os dados do array de floats para o buffer da OpenGl
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

	// Geração do identificador do VAO (Vertex Array Object)
	glGenVertexArrays(1, &VAO);
	// Vincula (bind) o VAO primeiro, e em seguida  conecta e seta o(s) buffer(s) de vértices
	// e os ponteiros para os atributos
	glBindVertexArray(VAO);
	// Para cada atributo do vertice, criamos um "AttribPointer" (ponteiro para o atributo), indicando:
	//  Localização no shader * (a localização dos atributos devem ser correspondentes no layout especificado no vertex shader)
	//  Numero de valores que o atributo tem (por ex, 3 coordenadas xyz)
	//  Tipo do dado
	//  Se está normalizado (entre zero e um)
	//  Tamanho em bytes
	//  Deslocamento a partir do byte zero
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), (GLvoid *)0);
	glEnableVertexAttribArray(0);

	// Observe que isso é permitido, a chamada para glVertexAttribPointer registrou o VBO como o objeto de buffer de vértice
	// atualmente vinculado - para que depois possamos desvincular com segurança
	glBindBuffer(GL_ARRAY_BUFFER, 0);

	// Desvincula o VAO (é uma boa prática desvincular qualquer buffer ou array para evitar bugs medonhos)
	glBindVertexArray(0);

	return VAO;
}