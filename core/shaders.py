from OpenGL.GL import *

class ShaderProgram:

    def __init__(self, vert_src, frag_src):
        self.program_id = self.create_program(vert_src, frag_src)

    def create_program(self, vert_src, frag_src):
        vs = self.compile_shader(vert_src, GL_VERTEX_SHADER)
        fs = self.compile_shader(frag_src, GL_FRAGMENT_SHADER)
        prog = glCreateProgram()
        glAttachShader(prog, vs)
        glAttachShader(prog, fs)
        glLinkProgram(prog)
        if not glGetProgramiv(prog, GL_LINK_STATUS):
            info_log = glGetProgramInfoLog(prog)
            raise RuntimeError(f"Shader link error: {info_log.decode('utf-8')}")
        glDetachShader(prog, vs)
        glDetachShader(prog, fs)
        glDeleteShader(vs)
        glDeleteShader(fs)
        return prog

    def compile_shader(self, source, shader_type):
        sid = glCreateShader(shader_type)
        glShaderSource(sid, source)
        glCompileShader(sid)
        if not glGetShaderiv(sid, GL_COMPILE_STATUS):
            info_log = glGetShaderInfoLog(sid)
            raise RuntimeError(f"Shader compile error: {info_log.decode('utf-8')}")
        return sid

    def use(self):
        glUseProgram(self.program_id)

    def unuse(self):
        glUseProgram(0)

    def set_uniform_matrix4fv(self, name, mat4):
        loc = glGetUniformLocation(self.program_id, name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, mat4)

    def set_uniform3f(self, name, x, y, z):
        loc = glGetUniformLocation(self.program_id, name)
        glUniform3f(loc, x, y, z)

    def set_uniform1i(self, name, value):
        loc = glGetUniformLocation(self.program_id, name)
        glUniform1i(loc, value)
