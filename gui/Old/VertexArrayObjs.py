from OpenGL.GL import *

#returns the elemType (OpenGL type) parameter's size in bytes
def get_size_of_type(elemType):
    if elemType == GL_FLOAT:
        return 4
    elif elemType == GL_UNSIGNED_INT:
        return 4
    elif elemType == GL_UNSIGNED_BYTE:
        return 1

#returns whether elemType (OpenGL type) parameter should be normalized
def get_normalized_of_type(elemType):
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

    #def __del__(self):
        #print("Destructor called: VBO")
        #try: 
            #glDeleteBuffers(1, self.ID)
        #except Exception as e:
            #print("Vertex Buffer deleteion fail")

    #binds the vertex buffer in OpenGL
    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.ID)

    #unbinds the vertex buffer in OpenGL
    def unbind(self):
        glBindBuffer(GL_ARRAY_BUFFER, GLuint(0))

class IndexBuffer:
    def __init__(self, data, count):
        self.ID = glGenBuffers(1)
        self.count = count
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, count * 4, data, GL_STATIC_DRAW)

    #def __del__(self):
        #print("Destructor called: IBO")
        #try:
            #glDeleteBuffers(1, self.ID)
        #except Exception as e:
            #print("Index Buffer deletion fail")

    #binds the index buffer in OpenGL
    def bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ID)

    #unbinds the index buffer in OpenGL
    def unbind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, GLuint(0))

class VertexBufferLayoutElement:
    def __init__(self, elemType, count, normalized):
        self.count = count
        self.normalized = normalized
        self.elemType = elemType

class VertexBufferLayout:
    def __init__(self):
        self.elements = []
        self.stride = 0

    #def __del__(self):
        #print("Destructor called: VBL")

    def push(self, elemType : constant, count: int):
        self.elements.append(VertexBufferLayoutElement(elemType, count, get_normalized_of_type(elemType)))
        self.stride += get_size_of_type(elemType) * count
        
class VertexArray:
    def __init__(self):
        self.ID = glGenVertexArrays(1)

    #def __del__(self):
        #print("Destructor called: VAO")
        #try:
            #glDeleteVertexArrays(1, self.ID)
        #except Exception as e:
            #print("Vertex Array deletion fail")
        
    #Binds the vertex buffer and its layout to the VertexArray
    def addBuffer(self, vb: VertexBuffer, layout: VertexBufferLayout):
        self.bind()
        vb.bind()
        i = 0
        offset = 0
        for element in layout.elements:
            glEnableVertexAttribArray(i)
            glVertexAttribPointer(i, element.count, element.elemType, element.normalized, layout.stride, GLvoidp(offset))
            i += 1
            offset += element.count * get_size_of_type(element.elemType)

    #Binds the vertex array in OpenGL
    def bind(self):
        glBindVertexArray(self.ID)

    #Unbinds the vertex array in OpenGL
    def unbind(self):
        glBindVertexArray(GLuint(0))
