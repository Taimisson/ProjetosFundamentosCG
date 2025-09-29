#ifndef SPRITE_H
#define SPRITE_H

#include <iostream>
#include <string>
#include <assert.h>

using namespace std;

// GLAD
#include <glad/glad.h>

// GLFW - porque inclui a OpenGL
#include <GLFW/glfw3.h>

// GLM
#include <glm/glm.hpp> 
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

using namespace glm;

class Sprite
{
    public:
        Sprite();
        ~Sprite();
        void initialize(GLuint shaderID, GLuint texID, vec3 pos, vec3 dimensions, float angle = 0.0);
        void update();
        void draw();

    private:
        GLuint VAO; //id do VAO da geometria
        GLuint texID; //id da textura
        vec3 pos; //posicao
        vec3 dimensions; //fatores de escala
        float angle; //angulo para rotação no eixo z
        GLuint shaderID; //para acessar o shader

        GLuint setupGeometry();

};

#endif