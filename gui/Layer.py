from TextureObj import TextureManager
from ShaderObj import Shader
from RendererObj import Renderer
from VertexArrayObjs import VertexArray, VertexBuffer, IndexBuffer, VertexBufferLayout
from OpenGL.GL import *

class vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return vec2D(x, y)
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return vec2D(x, y)
class Drawable:
    def __init__(self, pos: vec2D, center: vec2D, size: vec2D):
        self.pos = pos
        self.center = center
        self.size = size
class Button(Drawable):
    indices = [0, 1, 2, 2, 3, 0]
    indices_gl = (GLuint * len(indices))(*indices)

    def __init__(self, pos: vec2D, center: vec2D, size: vec2D, visibility: bool):
        super().__init__(pos, center, size)
        self.buttonChildren = []
        self.visibility = visibility
        self.visibilityChildren = False
        Button.shader = Shader("Texture.shader")
        Button.ib = IndexBuffer(Button.indices_gl, 6)
        bottomLeft = pos - center
        topRight = bottomLeft + size
        left = Renderer.normalizeWidth(bottomLeft.x)
        right = Renderer.normalizeWidth(topRight.x)
        top = Renderer.normalizeHeight(topRight.y)
        bottom = Renderer.normalizeHeight(bottomLeft.y)

        vertices = [left, bottom, 0.0, 0.0, 
                    right,bottom, 1.0, 0.0, 
                    right, top,   1.0, 1.0,
                    left,  top,   0.0, 1.0]
        vertices_gl = (GLfloat * len(vertices))(*vertices)
        self.vb = VertexBuffer(vertices_gl, 4 * 4 * 4)

        self.va = VertexArray()
        vbLayout = VertexBufferLayout()
        vbLayout.push(GL_FLOAT, 2)
        vbLayout.push(GL_FLOAT, 2)
        self.va.addBuffer(self.vb, vbLayout)

    def loadTexture(self, filepath: str):
        self.textureID = TextureManager.loadTexture(filepath)
    def draw(self):
        if self.visibility == True:
            TextureManager.bind(self.textureID, 0)
            Button.shader.bind()
            Button.shader.setUniform1i("u_Texture", 0)
            Renderer.draw(self.va, Button.ib, Button.shader)
    def addChildButtons(self, *args):
        for arg in args:
            self.buttonChildren.append(arg)
    def leftClickedDefault(self):
        if self.visibilityChildren == True:
            self.visibilityChildren = False
            for child in self.buttonChildren:
                child.visibility = True
        else:
            self.visibilityChildren = True
            for child in self.buttonChildren:
                child.visibility = False
    def leftClicked(function = leftClickedDefault, *args, **kargs):
        function(*args, **kargs) 
class Layer:
    def __init__(self, size: vec2D, topLeft: vec2D):
        self.topLeft = topLeft
        self.bottomRight = topLeft + size
        self.objects = []
        #self.m_activeTopLeft = vec2D(0, 0)
        #self.m_activeBottomLeft = vec2D(0, 0)
    @staticmethod
    def withinBounds(drawable: Drawable, x, y) -> bool:
        topLeft = drawable.pos - drawable.center
        bottomRight = topLeft + drawable.size
        if  x >= topLeft.x and x <= bottomRight.x and y >= topLeft.y and y <= bottomRight.y:
            return True
        else:
            return False

