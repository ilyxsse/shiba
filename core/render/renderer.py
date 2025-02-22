from core.render.background import BackgroundRenderer
from core.render.model import ModelRenderer

class Renderer:
    def __init__(self, width, height, texture_manager, model):
        self.width = width
        self.height = height
        self.texture_manager = texture_manager
        self.model = model
        self.bg_renderer = BackgroundRenderer()
        self.model_renderer = ModelRenderer(width, height, model)

    def draw_background(self):
        self.bg_renderer.draw(self.texture_manager)

    def draw_model(self, eye, target, up, rot_x, rot_y, light_dir, lighting_on):
        self.model_renderer.draw(eye, target, up, rot_x, rot_y, light_dir, lighting_on)