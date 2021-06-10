from OpenGL.GL import *

def getSizeOfType(elemType):
    if elemType == GL_FLOAT:
        return 4
    elif elemType == GL_UNSIGNED_INT:
        return 4
    elif elemType == GL_UNSIGNED_BYTE:
        return 1

def getNormalizedOftype(elemType):
    if elemType == GL_FLOAT:
        return GL_FALSE
    elif elemType == GL_UNSIGNED_INT:
        return GL_FALSE
    elif elemType == GL_UNSIGNED_BYTE:
        return GL_TRUE

class VertexBuffer:
    def __init__(self, data, size):
        self.ID = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.ID)
        glBufferData(GL_ARRAY_BUFFER, size, data, GL_STATIC_DRAW)
    def __del__(self):
        print("Destructor called: VBO")
        try: 
            glDeleteBuffers(1, self.ID)
        except Exception as e:
            print("Vertex Buffer deleteion fail")
    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.ID)
    def unbind(self):
        glBindBuffer(GL_ARRAY_BUFFER, GLuint(0))

class IndexBuffer:
    def __init__(self, data, count):
        self.ID = glGenBuffers(1)
        self.count = count
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, count * 4, data, GL_STATIC_DRAW)
    def __del__(self):
        print("Destructor called: IBO")
        try:
            glDeleteBuffers(1, self.ID)
        except Exception as e:
            print("Index Buffer deletion fail")
    def bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ID)
    def unbind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, GLuint(0))

class VertexBufferElement:
    def __init__(self, elemType, count, normalized):
        self.count = count
        self.normalized = normalized
        self.elemType = elemType

class VertexBufferLayout:
    def __init__(self):
        self.elements = []
        self.stride = 0
    def __del__(self):
        print("Destructor called: VBL")
    def push(self, elemType : constant, count: int):
        self.elements.append(VertexBufferElement(elemType, count, getNormalizedOftype(elemType)))
        self.stride += getSizeOfType(elemType) * count
        
class VertexArray:
    def __init__(self):
        self.ID = glGenVertexArrays(1)
    def __del__(self):
        print("Destructor called: VAO")
        try:
            glDeleteVertexArrays(1, self.ID)
        except Exception as e:
            print("Vertex Array deletion fail")
    def addBuffer(self, vb: VertexBuffer, layout: VertexBufferLayout):
        self.bind()
        vb.bind()
        i = 0
        offset = 0
        for element in layout.elements:
            glEnableVertexAttribArray(i)
            glVertexAttribPointer(i, element.count, element.elemType, element.normalized, layout.stride, GLvoidp(offset))
            i += 1
            offset += element.count * getSizeOfType(element.elemType)
    def bind(self):
        glBindVertexArray(self.ID)
    def unbind(self):
        glBindVertexArray(GLuint(0))