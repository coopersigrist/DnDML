import pyglet

from OpenGL.GL import *
from VertexArrayObjs import VertexArray, VertexBuffer, IndexBuffer, VertexBufferLayout
from ShaderObj import Shader
from RendererObj import Renderer
from TextureObj import Texture
from Layer import *

window = pyglet.window.Window(width = 1200, height = 800, caption = 'Test')

event_logger = pyglet.window.event.WindowEventLogger()
window.push_handlers(event_logger)

#vertices = [-0.5, -0.5, 0.0, 0.0, 
#             0.5, -0.5, 1.0, 0.0, 
#             0.5,  0.5, 1.0, 1.0,
#           -0.5,  0.5, 0.0, 1.0]
#vertices_gl = (GLfloat * len(vertices))(*vertices)

#vb = VertexBuffer(vertices_gl, 4 * 4 * 4)

#indices = [0, 1, 2, 2, 3, 0]
#indices_gl = (GLuint * len(indices))(*indices)

#ib = IndexBuffer(indices_gl, 6)

#va = VertexArray()
#vbLayout = VertexBufferLayout()
#vbLayout.push(GL_FLOAT, 2)
#vbLayout.push(GL_FLOAT, 2)
#va.addBuffer(vb, vbLayout)

#mainShader = Shader("Basic.shader")
#mainShader.bind()
#mainShader.setUniform4f("u_Color", 0.8, 0.3, 0.8, 1.0)

#texture = Texture("panther.png")
#texture.bind(0)
#mainShader.setUniform1i("u_Texture", 0)

#va.unbind()
#vb.unbind()
#ib.unbind()
#mainShader.unbind()
background = Button(vec2D(0, 0), vec2D(0, 0), vec2D(1200, 800), True)
background.loadTexture("plain_old.png")
theButton = Button(vec2D(0, 750), vec2D(0, 0), vec2D(150, 50), True)
theButton.loadTexture("button.png")
aButton = Button(vec2D(50, 700), vec2D(0, 0), vec2D(100, 50), False)
aButton.loadTexture("button.png")
aButton1 = Button(vec2D(50, 650), vec2D(0, 0), vec2D(100, 50), False)
aButton1.loadTexture("button.png")
theButton.addChildButtons(aButton, aButton1)

@window.event
def on_draw():
    global r
    global increment
    window.clear()
    
    Renderer.clear()
    background.draw()
    theButton.draw()
    aButton.draw()
    aButton1.draw()

def update(dt):
    pass

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT :
        if Layer.withinBounds(theButton, x, y):
            theButton.leftClickedDefault()
pyglet.app.run()