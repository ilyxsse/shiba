from OpenGL.GL import *

class PrimitiveData:
    """
    holds VAO, 
    index count, 
    and texture ID for one glTF primitive
    """
    def __init__(self, vao, index_count, texture_id):
        self.vao = vao
        self.index_count = index_count
        self.texture_id = texture_id

    def draw(self):
        if self.texture_id:
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.index_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        if self.texture_id:
            glBindTexture(GL_TEXTURE_2D, 0)
