import ctypes
import numpy as np
from OpenGL.GL import *
from pygltflib import GLTF2
from PIL import Image

from core.gltf.loader import load_accessor_data, load_image_from_gltf
from core.gltf.primitive import PrimitiveData

class GLTFModel:
    """
    loads the model, 
    auto-centers and scales it to fit,
    and prepares VAOs for rendering
    """
    def __init__(self, path):
        self.primitives = []
        self.load_model(path)

    def load_model(self, path):
        gltf = GLTF2().load(path)
        min_bounds = np.array([np.inf, np.inf, np.inf], dtype=np.float32)
        max_bounds = np.array([-np.inf, -np.inf, -np.inf], dtype=np.float32)
        raw_primitives = []
        for mesh in gltf.meshes:
            for prim in mesh.primitives:
                pos_data = load_accessor_data(gltf, prim.attributes.POSITION)
                if hasattr(prim.attributes, "NORMAL") and prim.attributes.NORMAL is not None:
                    nor_data = load_accessor_data(gltf, prim.attributes.NORMAL)
                else:
                    nor_data = np.zeros_like(pos_data)
                if hasattr(prim.attributes, "TEXCOORD_0") and prim.attributes.TEXCOORD_0 is not None:
                    uv_data = load_accessor_data(gltf, prim.attributes.TEXCOORD_0)
                else:
                    uv_data = np.zeros((pos_data.shape[0], 2), dtype=np.float32)
                idx_data = load_accessor_data(gltf, prim.indices).flatten().astype(np.uint32)
                min_bounds = np.minimum(min_bounds, pos_data.min(axis=0))
                max_bounds = np.maximum(max_bounds, pos_data.max(axis=0))
                raw_primitives.append({
                    "pos_data": pos_data,
                    "nor_data": nor_data,
                    "uv_data": uv_data,
                    "idx_data": idx_data,
                    "material_index": prim.material
                })
        center = (min_bounds + max_bounds) / 2.0
        largest_dim = (max_bounds - min_bounds).max()
        if largest_dim < 1e-9:
            largest_dim = 1.0
        scale = 2.0 / largest_dim
        final_primitives = []
        for p in raw_primitives:
            pos_data = (p["pos_data"] - center) * scale
            nor_data = p["nor_data"]
            uv_data = p["uv_data"]
            idx_data = p["idx_data"]
            material_index = p["material_index"]

            vertex_data = np.hstack([pos_data, nor_data, uv_data]).astype(np.float32)
            vao = glGenVertexArrays(1)
            glBindVertexArray(vao)
            vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
            ebo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, idx_data.nbytes, idx_data, GL_STATIC_DRAW)
            stride = 8 * vertex_data.itemsize  # 3 for pos, 3 for normal, 2 for uv
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * vertex_data.itemsize))
            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * vertex_data.itemsize))
            glBindVertexArray(0)
            texture_id = self.load_material_texture(gltf, material_index)
            final_primitives.append(PrimitiveData(vao, len(idx_data), texture_id))
        self.primitives = final_primitives

    def load_material_texture(self, gltf, material_index):
        if material_index is None or material_index < 0:
            return self.create_white_texture()
        mat = gltf.materials[material_index]
        mr = mat.pbrMetallicRoughness
        if mr and mr.baseColorTexture:
            tex_index = mr.baseColorTexture.index
            tex_obj = gltf.textures[tex_index]
            image_index = tex_obj.source
            pil_img = load_image_from_gltf(gltf, image_index)
            if pil_img:
                pil_img = pil_img.convert("RGB")
                pil_img = pil_img.transpose(Image.FLIP_TOP_BOTTOM)
                w, h = pil_img.size
                img_data = pil_img.tobytes("raw", "RGB", 0, -1)
                tex_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, tex_id)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
                glGenerateMipmap(GL_TEXTURE_2D)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                return tex_id
            else:
                return self.create_white_texture()
        else:
            return self.create_white_texture()

    def create_white_texture(self):
        white_pixel = np.array([255, 255, 255], dtype=np.uint8)
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 1, 1, 0, GL_RGB, GL_UNSIGNED_BYTE, white_pixel)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return tex_id

    def draw(self):
        for prim in self.primitives:
            prim.draw()