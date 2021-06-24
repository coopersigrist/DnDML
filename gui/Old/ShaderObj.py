from OpenGL.GL import *

class Shader:

    def __init__(self, filepath: str):
        srcs = self.parse_shader(filepath)
        self.cache = {}
        self.ID = self.create_shader(srcs[0], srcs[1])

    def __del__(self):
        #glDeleteProgram(self.ID)
        pass

    #Bind this shader in OpenGL for rendering
    def bind(self):
        glUseProgram(self.ID)

    #Unbinds any shader currently bound in OpenGL 
    def unbind(self):
        glUseProgram(GLuint(0))

    #Sets 1 integer uniform in the shader
    def set_uniform1i(self, name: str, i0: int):
        glUniform1i(self.get_uniform_location(name), i0)

    #Sets 4 floats uniforms in the shader
    def set_uniform4f(self, name: str, f0: float, f1: float, f2: float, f3: float):
        glUniform4f(self.get_uniform_location(name), f0, f1, f2, f3)

    #PRIVATE: retrieves the location of a uniform in the shader given its name
    def get_uniform_location(self, name: str):
        if name in self.cache:
            return self.cache[name]
        else:
            location = glGetUniformLocation(self.ID, name)
            if location == -1:
                print("Uniform " + name + " does not exist")
            self.cache[name] = location
            return location

    #PRIVATE: Creates a shader program given GLSL source code and shader type. Prints error messages 
    #         if there is a compilation error 
    def compile_shader(self, shaderType: constant, src: str):
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

    #PRIVATE: Creates a "OpenGL program" given a vertex and fragment shaders' source codes.
    def create_shader(self, vertexShader: str, fragmentShader: str):
        program = glCreateProgram()
        vs = self.compile_shader(GL_VERTEX_SHADER, vertexShader)
        fs = self.compile_shader(GL_FRAGMENT_SHADER, fragmentShader)
        glAttachShader(program, vs)
        glAttachShader(program, fs)
        glLinkProgram(program)
        glValidateProgram(program)
        glDeleteShader(vs)
        glDeleteShader(fs)
        return program

    #PRIVATE: Loads and returns a list of strings of GLSL source code with different shader types given a filepath.
    #         The source code must contain "tags": '#shader vertex' and '#shader fragment" to distinguish
    #         the starting points of the different shader types' source codes
    def parse_shader(self, filepath: str)-> list:
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