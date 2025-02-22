import pygame
from OpenGL.GL import *

class TextureManager:

    def __init__(self):
        self.textures = {}
        self.init_textures()

    def init_textures(self):
        path = "assets/background.png"
        try:
            surface = pygame.image.load(path).convert_alpha()
        except Exception as e:
            raise RuntimeError(f"Could not load background: {e}")
        w, h = surface.get_size()
        data = pygame.image.tostring(surface, "RGB", True)
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.textures["background"] = tex_id
