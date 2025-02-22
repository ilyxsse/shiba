import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from src.controller import EventHandler
from core.texturer import TextureManager
from core.render.renderer import Renderer
from core.gltf.mesh import GLTFModel

class ShibaApp:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width, self.height = width, height

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        glViewport(0, 0, width, height)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

        self.event_handler = EventHandler()
        self.texture_manager = TextureManager()
        self.model = GLTFModel("assets/model.glb")
        self.renderer = Renderer(self.width, self.height, self.texture_manager, self.model)

        self.rot_x = 0.0
        self.rot_y = 0.0

    def run(self):
        print("Welcome to Shiba!")
        print("Press 'T' to toggle lighting on, use arrow keys to change the direction. Use the mouse wheel to zoom in.")

        clock = pygame.time.Clock()
        running = True
        while running:
            events = pygame.event.get()
            running = self.event_handler.handle_events(events)

            dx, dy = self.event_handler.mouse_delta
            self.rot_y += dx * 0.3
            self.rot_x += dy * 0.3

            glClearColor(0.1, 0.1, 0.1, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.renderer.draw_background()
            self.renderer.draw_model(
                eye=(0, 0, self.event_handler.zoom),
                target=(0, 0, 0),
                up=(0, 1, 0),
                rot_x=self.rot_x,
                rot_y=self.rot_y,
                light_dir=self.event_handler.light_dir,
                lighting_on=self.event_handler.lighting_on
            )

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    ShibaApp().run()