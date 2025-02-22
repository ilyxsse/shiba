import math
from OpenGL.GL import *
from pyrr import Matrix44, Vector3
from core.shaders import ShaderProgram

MODEL_VERT_SRC = r"""
#version 330 core
layout(location = 0) in vec3 inPos;
layout(location = 1) in vec3 inNormal;
layout(location = 2) in vec2 inUV;

uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProj;

out vec3 vNormal;
out vec2 vUV;

void main() {
    gl_Position = uProj * uView * uModel * vec4(inPos, 1.0);
    vNormal = mat3(uModel) * inNormal;
    vUV = inUV;
}
"""

MODEL_FRAG_SRC = r"""
#version 330 core
in vec3 vNormal;
in vec2 vUV;
out vec4 outColor;

uniform sampler2D uTexture;
uniform vec3 uLightDir;
uniform vec3 uLightColor;
uniform vec3 uAmbient;
uniform bool uLightingOn;

void main() {
    vec4 texColor = texture(uTexture, vUV);
    if(uLightingOn) {
        vec3 N = normalize(vNormal);
        vec3 L = normalize(-uLightDir);
        float diff = max(dot(N, L), 0.0);
        vec3 lighting = uAmbient + uLightColor * diff;
        outColor = vec4(lighting, 1.0) * texColor;
    } else {
        outColor = texColor;
    }
}
"""

class ModelRenderer:
    def __init__(self, width, height, model):
        self.width = width
        self.height = height
        self.model = model
        self.shader = ShaderProgram(MODEL_VERT_SRC, MODEL_FRAG_SRC)

    def draw(self, eye, target, up, rot_x, rot_y, light_dir, lighting_on):
        view_mat = Matrix44.look_at(Vector3(eye), Vector3(target), Vector3(up))
        proj_mat = Matrix44.perspective_projection(45.0, float(self.width) / self.height, 0.1, 100.0)
        rx_mat = Matrix44.from_x_rotation(math.radians(rot_x))
        ry_mat = Matrix44.from_y_rotation(math.radians(rot_y))
        model_mat = rx_mat @ ry_mat

        self.shader.use()
        loc_model = glGetUniformLocation(self.shader.program_id, "uModel")
        glUniformMatrix4fv(loc_model, 1, GL_FALSE, model_mat.astype('float32').tobytes())
        loc_view = glGetUniformLocation(self.shader.program_id, "uView")
        glUniformMatrix4fv(loc_view, 1, GL_FALSE, view_mat.astype('float32').tobytes())
        loc_proj = glGetUniformLocation(self.shader.program_id, "uProj")
        glUniformMatrix4fv(loc_proj, 1, GL_FALSE, proj_mat.astype('float32').tobytes())

        loc_lightdir = glGetUniformLocation(self.shader.program_id, "uLightDir")
        glUniform3f(loc_lightdir, light_dir[0], light_dir[1], light_dir[2])
        loc_lightcolor = glGetUniformLocation(self.shader.program_id, "uLightColor")
        glUniform3f(loc_lightcolor, 1.0, 1.0, 1.0)
        loc_ambient = glGetUniformLocation(self.shader.program_id, "uAmbient")
        glUniform3f(loc_ambient, 0.2, 0.2, 0.2)
        loc_lighting = glGetUniformLocation(self.shader.program_id, "uLightingOn")
        glUniform1i(loc_lighting, 1 if lighting_on else 0)

        # each primitive binds its own texture
        self.model.draw()
        self.shader.unuse()