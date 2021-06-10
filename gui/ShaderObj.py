from OpenGL.GL import *

class Shader:
    def __init__(self, filepath: str):
        srcs = self.parseShader(filepath)
        self.cache = {}
        self.ID = self.createShader(srcs[0], srcs[1])
    def __del__(self):
        glDeleteProgram(self.ID)
    def bind(self):
        glUseProgram(self.ID)
    def unbind(self):
        glUseProgram(GLuint(0))
    def setUniform1i(self, name: str, i0: int):
        glUniform1i(self.getUniformLocation(name), i0)
    def setUniform4f(self, name: str, f0: float, f1: float, f2: float, f3: float):
        glUniform4f(self.getUniformLocation(name), f0, f1, f2, f3)
    def getUniformLocation(self, name: str):
        if name in self.cache:
            return self.cache[name]
        else:
            location = glGetUniformLocation(self.ID, name)
            if location == -1:
                print("Uniform " + name + " does not exist")
            self.cache[name] = location
            return location
    def compileShader(self, shaderType: constant, src: str):
        id = glCreateShader(shaderType)
        glShaderSource(id, src)
        glCompileShader(id)
        result = glGetShaderiv(id, GL_COMPILE_STATUS)
        if result == GL_FALSE:
            length = glGetShaderiv(id, GL_INFO_LOG_LENGTH)
            msg = glGetShaderInfoLog(id)
            print(msg)
            glDeleteShader(id)
        return id
    def createShader(self, vertexShader: str, fragmentShader: str):
        program = glCreateProgram()
        vs = self.compileShader(GL_VERTEX_SHADER, vertexShader)
        fs = self.compileShader(GL_FRAGMENT_SHADER, fragmentShader)
        glAttachShader(program, vs)
        glAttachShader(program, fs)
        glLinkProgram(program)
        glValidateProgram(program)
        glDeleteShader(vs)
        glDeleteShader(fs)
        return program
    def parseShader(self, filepath: str)-> list:
        shaders = ["", ""]
        mode = 0
        with open(filepath) as file:
            for line in file:
                if line.find("#shader") != -1:
                    if line.find("vertex") != -1:
                        mode = 0
                    elif line.find("fragment") != -1:
                        mode = 1
                else:
                    shaders[mode] += line
        return shaders