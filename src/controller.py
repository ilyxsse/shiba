import pygame
from pygame.locals import *

class EventHandler:
    def __init__(self):
        self.running = True
        self.mouse_down = False
        self.last_mouse_pos = None
        self.mouse_delta = (0, 0)

        self.zoom = 5.0
        self.light_dir = [1, 0, 0]
        self.lighting_on = False

    def handle_events(self, events):
        self.mouse_delta = (0, 0)
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                self.lighting_on = not self.lighting_on
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_down = True
                    self.last_mouse_pos = event.pos
                elif event.button == 4:
                    self.zoom = max(1.0, self.zoom - 0.5)
                elif event.button == 5:
                    self.zoom += 0.5
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_down = False
                    self.last_mouse_pos = None
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_down and self.last_mouse_pos:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.mouse_delta = (dx, dy)
                    self.last_mouse_pos = event.pos

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.light_dir[0] -= 0.05
        if keys[pygame.K_RIGHT]:
            self.light_dir[0] += 0.05
        if keys[pygame.K_UP]:
            self.light_dir[1] += 0.05
        if keys[pygame.K_DOWN]:
            self.light_dir[1] -= 0.05

        return True