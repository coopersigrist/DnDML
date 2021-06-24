import pyglet

#Creating an OpenGL context and a window before the rest of the GUI is initialized
display = pyglet.canvas.get_display()
screen = display.get_default_screen()
window = pyglet.window.Window(screen.width, screen.height, caption = 'DNDML', fullscreen=True)

#logs pyglet events in the console
#event_logger = pyglet.window.event.WindowEventLogger()
#window.push_handlers(event_logger)

from OpenGL.GL import *
from VertexArrayObjs import VertexArray, VertexBuffer, IndexBuffer, VertexBufferLayout
from ShaderObj import Shader
from RendererObj import Renderer
from TextureObj import Texture
from DrawableObjs import TexturedRectangle, StrokedButton, Button, VerticalBar
from Layer import *


glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


background = TexturedRectangle(Vec2D(0, 0), Vec2D(0, 0), Vec2D(Renderer.inputWidth, Renderer.inputHeight), True, "desktop1.png")

expandable1 = StrokedButton(Vec2D(65, 133), Vec2D(0, 0), Vec2D(174, 40), 
                            Vec2D(73.35, 156), Vec2D(0, 0), Vec2D(15, 10.35), "button.png")

button1 = Button(Vec2D(75, 173), Vec2D(0, 0), Vec2D(174, 30), AlarmManager.get_new_ID(), False, "button.png")

expandable1.add_button(button1)

expandable2 = StrokedButton(Vec2D(65, 173), Vec2D(0, 0), Vec2D(174, 40), 
                            Vec2D(73.35, 196), Vec2D(0, 0), Vec2D(15, 10.35), "button.png")

button2 = Button(Vec2D(75, 213), Vec2D(0, 0), Vec2D(174, 30), AlarmManager.get_new_ID(), False, "button.png")

expandable2.add_button(button2)

listOfButtons1 = []
listOfButtons1.append(expandable1)
listOfButtons1.append(expandable2)

theVerticalBar = VerticalBar(Vec2D(25, 25), listOfButtons1)

@window.event
#this method runs in every frame in pyglet application loop
def on_draw():
    window.clear()
    
    Renderer.clear()
    background.draw()
    theVerticalBar.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    
    theVerticalBar.left_clicked(Vec2D(x / screen.width * Renderer.inputWidth, (screen.height - y) / screen.height * Renderer.inputHeight))


pyglet.app.run()