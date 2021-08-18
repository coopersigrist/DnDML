from OpenGL.GL import *
from VertexArrayObjs import VertexArray, VertexBuffer, IndexBuffer, VertexBufferLayout
from ShaderObj import Shader
import pyglet

#A simple 2D vector for easier code
class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2D(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vec2D(x, y)

    def __truediv__(self, other: int):
        x = self.x / other
        y = self.y / other
        return Vec2D(x, y)
    
    def __str__(self):
        return str(self.x) + " " + str(self.y)

class Renderer:
    inputWidth = 1440
    inputHeight = 1024

    def __init__(self):
        pass

    #Renders stuff to the current window a VertexArray, IndexBuffer, and Shader objects. Note that to 
    #draw a texture, it must be independently bound before this function is called
    @staticmethod
    def draw(va: VertexArray, ib: IndexBuffer, shader: Shader):
        shader.bind()
        ib.bind()
        va.bind()
        glDrawElements(GL_TRIANGLES, ib.count, GL_UNSIGNED_INT, GLvoidp(0))

    #Clears everything drawn on the window
    @staticmethod
    def clear():
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    #Converts from this library's coordinate system with its center at the top left corner of the window and
    #Figma's UI model's size to the OpenGL system with numbers
    #that range from -1 to 1 with its origin at the center of the window
    @staticmethod
    def to_openGL_coordinates(coor: Vec2D):
        return Vec2D(coor.x * 2 / Renderer.inputWidth - 1, -coor.y * 2 / Renderer.inputHeight + 1)


