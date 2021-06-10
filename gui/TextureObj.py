from OpenGL.GL import *
import PIL
from PIL import Image
class Texture:
    def __init__(self, path: str):
        self.filepath = path
        self.img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        self.width, self.height = self.img.size

        self.ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.ID)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.img.tobytes())
        glBindTexture(GL_TEXTURE_2D, GLuint(0))
    def __del__(self):
        glDeleteTextures(1, self.ID)
    def bind(self, slot):
        glActiveTexture(GL_TEXTURE0 + slot)
        glBindTexture(GL_TEXTURE_2D, self.ID)
    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, GLuint(0))
class TextureManager:
    size = 0
    textures = {}
    def __init__():
        pass
    @staticmethod
    def loadTexture(filepath: str):
        newTexture = Texture(filepath)
        TextureManager.textures[newTexture.ID] = newTexture
        return newTexture.ID
    @staticmethod
    def bind(ID, slot):
        TextureManager.textures[ID].bind(slot)
    @staticmethod
    def unbind():
        glBindTexture(GL_TEXTURE_2D, GLuint(0))