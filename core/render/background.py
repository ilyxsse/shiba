import ctypes
import numpy as np
from OpenGL.GL import *
from core.shaders import ShaderProgram

BG_VERT_SRC = r"""
#version 330 core
layout(location = 0) in vec2 inPos;
layout(location = 1) in vec2 inUV;
out vec2 vUV;
void main() {
    vUV = inUV;
    gl_Position = vec4(inPos, 0.0, 1.0);
}
"""

BG_FRAG_SRC = r"""
#version 330 core
in vec2 vUV;
out vec4 outColor;
uniform sampler2D bgTex;
void main() {
    outColor = texture(bgTex, vUV);
}
"""

class BackgroundRenderer:
    def __init__(self):
        self.shader = ShaderProgram(BG_VERT_SRC, BG_FRAG_SRC)
        self.vao, self.index_count = self.create_background_quad()

    def create_background_quad(self):
        verts = np.array([
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
             1.0,  1.0, 1.0, 1.0,
            -1.0,  1.0, 0.0, 1.0,
        ], dtype=np.float32)
        indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, verts.nbytes, verts, GL_STATIC_DRAW)
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        stride = 4 * verts.itemsize
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(2 * verts.itemsize))
        glBindVertexArray(0)
        return vao, len(indices)

    def draw(self, texture_manager):
        glDepthMask(GL_FALSE)
        self.shader.use()
        glBindVertexArray(self.vao)
        glActiveTexture(GL_TEXTURE0)
        bg_tex = texture_manager.textures["background"]
        glBindTexture(GL_TEXTURE_2D, bg_tex)
        loc = glGetUniformLocation(self.shader.program_id, "bgTex")
        glUniform1i(loc, 0)
        glDrawElements(GL_TRIANGLES, self.index_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        self.shader.unuse()
        glDepthMask(GL_TRUE)