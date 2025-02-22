import io
import numpy as np
from pygltflib import GLTF2
from PIL import Image

def load_accessor_data(gltf, accessor_index):
    accessor = gltf.accessors[accessor_index]
    bv = gltf.bufferViews[accessor.bufferView]
    buf = gltf.buffers[bv.buffer]
    if gltf.binary_blob is not None:
        buffer_data = gltf.binary_blob() if callable(gltf.binary_blob) else gltf.binary_blob
    else:
        with open(buf.uri, "rb") as f:
            buffer_data = f.read()
    start = (bv.byteOffset or 0) + (accessor.byteOffset or 0)
    component_type_map = {
        5126: (np.float32, 4),
        5123: (np.uint16, 2),
        5125: (np.uint32, 4),
    }
    dtype, csize = component_type_map[accessor.componentType]
    type_map = {
        "SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4,
        "MAT2": 4, "MAT3": 9, "MAT4": 16
    }
    num_components = type_map[accessor.type]
    count = accessor.count
    element_size = csize * num_components
    stride = bv.byteStride if bv.byteStride else element_size
    out = np.zeros((count, num_components), dtype=dtype)
    for i in range(count):
        offset = start + i * stride
        chunk = buffer_data[offset: offset + element_size]
        out[i] = np.frombuffer(chunk, dtype=dtype, count=num_components)
    return out

def load_image_from_gltf(gltf, image_index):
    image = gltf.images[image_index]
    if image.bufferView is not None:
        bv = gltf.bufferViews[image.bufferView]
        if gltf.binary_blob is not None:
            buffer_data = gltf.binary_blob() if callable(gltf.binary_blob) else gltf.binary_blob
        else:
            buf = gltf.buffers[bv.buffer]
            with open(buf.uri, "rb") as f:
                buffer_data = f.read()
        offset = bv.byteOffset or 0
        length = bv.byteLength
        raw = buffer_data[offset:offset+length]
        return Image.open(io.BytesIO(raw))
    elif image.uri is not None:
        if image.uri.startswith("data:"):
            import base64
            header, b64_data = image.uri.split(",", 1)
            raw = base64.b64decode(b64_data)
            return Image.open(io.BytesIO(raw))
        else:
            return Image.open(image.uri)
    else:
        return None