from Layer import AlarmManager
from TextureObj import TextureManager
from ShaderObj import Shader
from RendererObj import Renderer, Vec2D
from VertexArrayObjs import VertexArray, VertexBuffer, IndexBuffer, VertexBufferLayout
from OpenGL.GL import *

class Drawable:

    def __init__(self, pos: Vec2D, center: Vec2D, size: Vec2D, visibility: True):
        self.pos = pos
        self.center = center
        self.size = size
        self.visibility = visibility
        self.topLeft = pos - center
        self.bottomRight = self.topLeft + size

    def draw():
        raise NotImplementedError()

    def within_bounds(self, coordinates: Vec2D):
        if coordinates.x > self.topLeft.x and coordinates.x < self.bottomRight.x:
            if coordinates.y > self.topLeft.y and coordinates.y < self.bottomRight.y:
                return True
        return False
        
class TexturedRectangle(Drawable):
    indices = [0, 1, 2, 2, 3, 0]
    indicesGL = (GLuint * len(indices))(*indices)
    shader = Shader("Texture.shader")
    ib = IndexBuffer(indicesGL, 6)

    def __init__(self, pos: Vec2D, center: Vec2D, size: Vec2D, visibility: True, texturePath = None):
        super().__init__(pos, center, size, visibility)
        self.shouldComputeVerticesAgain = False
        
        topLeftGL = Renderer.to_openGL_coordinates(self.topLeft)
        bottomRightGL = Renderer.to_openGL_coordinates(self.bottomRight)

        vertices = [topLeftGL.x, bottomRightGL.y, 0.0, 0.0, 
                    bottomRightGL.x ,  bottomRightGL.y, 1.0, 0.0, 
                    bottomRightGL.x, topLeftGL.y,   1.0, 1.0,
                    topLeftGL.x,  topLeftGL.y,   0.0, 1.0]

        verticesGL = (GLfloat * len(vertices))(*vertices)
        self.vb = VertexBuffer(verticesGL, 4 * 4 * 4)
        self.va = VertexArray()
        vbLayout = VertexBufferLayout()
        vbLayout.push(GL_FLOAT, 2)
        vbLayout.push(GL_FLOAT, 2)
        self.va.addBuffer(self.vb, vbLayout)

        if texturePath != None:
            self.load_texture(texturePath)

    def load_texture(self, filepath: str):
        self.textureID = TextureManager.load_texture(filepath)

    def draw(self):
        if self.shouldComputeVerticesAgain:
            topLeftGL = Renderer.to_openGL_coordinates(self.topLeft)
            bottomRightGL = Renderer.to_openGL_coordinates(self.bottomRight)

            vertices = [topLeftGL.x, bottomRightGL.y, 0.0, 0.0, 
                        bottomRightGL.x ,  bottomRightGL.y, 1.0, 0.0, 
                        bottomRightGL.x, topLeftGL.y,   1.0, 1.0,
                        topLeftGL.x,  topLeftGL.y,   0.0, 1.0]

            verticesGL = (GLfloat * len(vertices))(*vertices)
            self.vb = VertexBuffer(verticesGL, 4 * 4 * 4)
            self.va = VertexArray()
            vbLayout = VertexBufferLayout()
            vbLayout.push(GL_FLOAT, 2)
            vbLayout.push(GL_FLOAT, 2)
            self.va.addBuffer(self.vb, vbLayout)
            self.shouldComputeVerticesAgain = True
        if self.visibility == True:
            TextureManager.bind(self.textureID, 0)
            TexturedRectangle.shader.bind()
            TexturedRectangle.shader.set_uniform1i("u_Texture", 0)
            Renderer.draw(self.va, TexturedRectangle.ib, TexturedRectangle.shader)

    def change_pos(self, newCoordinates: Vec2D):
        self.pos = newCoordinates
        self.shouldComputeVerticesAgain = True

class Button(TexturedRectangle):

    def __init__(self, pos: Vec2D, center: Vec2D, size: Vec2D, alarmID, visibility: True, texturePath = None):
        super().__init__(pos, center, size, visibility, texturePath)

        self.alarmID = alarmID

    def left_clicked(self, coordinates: Vec2D):
        if self.within_bounds(coordinates):
            AlarmManager.set_alarm(self.alarmID, True)
            return True
        return False

class StrokedButton(Drawable):

    def __init__(self, pos: Vec2D, center: Vec2D, size: Vec2D, strokePos: Vec2D, strokeCenter: Vec2D, strokeSize: Vec2D,
                texturePath = None):
        super().__init__(pos, center, size, True)
        self.ifExpanded = False
        self.expandedTopLeft = self.topLeft
        self.expandedBottomRight = self.bottomRight
        self.mainButton = TexturedRectangle(pos, center, size, True, texturePath)
        self.strokeButton = TexturedRectangle(strokePos, strokeCenter, strokeSize, True, "Stroke.png")
        self.otherButtons = []

    def within_bounds(self, coordinates: Vec2D):
        if self.ifExpanded == False:
            return super().within_bounds(coordinates)
        else: 
            if coordinates.x > self.expandedTopLeft.x and coordinates.x < self.expandedBottomRight.x:
                if coordinates.y > self.expandedTopLeft.y and coordinates.y < self.expandedBottomRight.y:
                    return True
            return False
    
    def draw(self):
        self.mainButton.draw()
        self.strokeButton.draw()
        if self.ifExpanded == True:
            for button in self.otherButtons:
                button.draw()

    def add_button(self, aButton: Drawable):
        self.otherButtons.append(aButton)
        aButton.visibility = False
        if aButton.topLeft.x < self.expandedTopLeft.x:
            self.expandedTopLeft.x = aButton.topLeft.x
        if aButton.topLeft.y < self.expandedTopLeft.y:
            self.expandedTopLeft.y = aButton.topLeft.y
        if aButton.bottomRight.x > self.expandedBottomRight.x:
            self.expandedBottomRight.x = aButton.bottomRight.x
        if aButton.bottomRight.y > self.expandedBottomRight.y:
            self.expandedBottomRight.y = aButton.bottomRight.y

    def left_clicked(self, coordinates: Vec2D):
        if not self.within_bounds(coordinates):
            return False
        elif self.strokeButton.within_bounds(coordinates):
            if self.ifExpanded:
                self.ifExpanded = False
                for button in self.otherButtons:
                    button.visibility = False
            else:
                self.ifExpanded = True
                for button in self.otherButtons:
                    button.visibility = True
            return True
        else:
            for button in self.otherButtons: 
                if button.left_clicked(coordinates):
                    return True
            return False

    def change_pos(self, newCoordinates: Vec2D):
        offset = newCoordinates - self.pos

        self.mainButton.change_pos(self.mainButton.pos + offset)
        self.strokeButton.change_pos(self.strokeButton.pos + offset)

        for button in self.otherButtons:
            button.change_pos(button.pos + offset)

class VerticalBar:

    #listOfButtons should only include Buttons or StrokedButtons
    def __init__(self, pos: Vec2D, listOfButtons: list):
        self.pos = pos
        self.listOfButtons = listOfButtons
        self.shouldEvaluatePos = False
    
    def left_clicked(self, coordinates: Vec2D):
        for button in self.listOfButtons:
            if isinstance(button, StrokedButton):
                ifExpandedBefore = button.ifExpanded
                if button.left_clicked(coordinates):
                    if button.ifExpanded != ifExpandedBefore:
                        self.shouldEvaluatePos = True
                    return True
            else:
                if button.left_clicked(coordinates):
                    return True
        return False

    #ListOfButtons should have at least one button
    def draw(self):
        if self.shouldEvaluatePos:
            prevY = self.listOfButtons[0].pos.y
            for button in self.listOfButtons:
                button.change_pos(Vec2D(button.pos.x, prevY))
                if isinstance(button, StrokedButton) and button.ifExpanded:
                    prevY = button.expandedBottomRight.y
                else:
                    prevY = button.bottomRight.y
            self.shouldEvaluatePos = False
        for button in self.listOfButtons:
            button.draw()



    

    

                    

            

