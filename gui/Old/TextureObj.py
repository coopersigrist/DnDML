from OpenGL.GL import *
import PIL
from PIL import Image

#It is discouraged to initialize this Texture class on its own
class Texture:
    def __init__(self, img):
        self.width, self.height = img.size

        self.ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.ID)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())
        glBindTexture(GL_TEXTURE_2D, GLuint(0))

    def __del__(self):
        #glDeleteTextures(1, self.ID)
        pass

    def bind(self, slot):
        glActiveTexture(GL_TEXTURE0 + slot)
        glBindTexture(GL_TEXTURE_2D, self.ID)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, GLuint(0))

class TextureManager:
    size = 0
    #Keeps track of the IDs of allocated Texture objects
    textures = {}
    #Keeping track of images already loaded
    images = {}
    def __init__():
        pass

    @staticmethod
    #Loads an image given a filepath and returns an ID to a texture object with the image
    def load_texture(filepath: str):
        if filepath not in TextureManager.images:
            TextureManager.images[filepath] = Image.open(filepath).transpose(Image.FLIP_TOP_BOTTOM)
        newTexture = Texture(TextureManager.images[filepath])
        TextureManager.textures[newTexture.ID] = newTexture
        return newTexture.ID

    @staticmethod
    #Bind the texture with the ID to a slot in OpenGL for rendering
    def bind(ID, slot):
        TextureManager.textures[ID].bind(slot)

    #Unbinds any currently bound texture
    @staticmethod
    def unbind():
        glBindTexture(GL_TEXTURE_2D, GLuint(0))