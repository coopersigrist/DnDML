from OpenGL.GL import *
from VertexArrayObjs import VertexArray, VertexBuffer, IndexBuffer, VertexBufferLayout
from ShaderObj import Shader
import pyglet

class Renderer:
    screenWidth = 1200
    screenHeight = 800
    def __init__(self):
        pass
    @staticmethod
    def draw(va: VertexArray, ib: IndexBuffer, shader: Shader):
        shader.bind()
        ib.bind()
        va.bind()
        glDrawElements(GL_TRIANGLES, ib.count, GL_UNSIGNED_INT, GLvoidp(0))
    @staticmethod
    def clear():
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    @staticmethod
    def normalizeWidth(width):
        return (width * 2 / Renderer.screenWidth) - 1
    @staticmethod
    def normalizeHeight(height):
        return (height * 2 / Renderer.screenHeight) - 1
