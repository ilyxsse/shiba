from pygltflib import GLTF2
import base64

gltf = GLTF2().load("assets/model.glb")

if not gltf.materials:
    print("No materials found.")
else:
    print(f"Found {len(gltf.materials)} material(s):\n")
    glb_file_path = "assets/model.glb"
    with open(glb_file_path, "rb") as f:
        glb_data = f.read()

    for idx, material in enumerate(gltf.materials):
        print(f"Material {idx + 1}:")
        pbr = material.pbrMetallicRoughness
        if pbr.baseColorTexture:
            texture_index = pbr.baseColorTexture.index
            print(f" - baseColorTexture index: {texture_index}")
            if gltf.textures and len(gltf.textures) > texture_index:
                image_index = gltf.textures[texture_index].source
                if gltf.images and len(gltf.images) > image_index:
                    image = gltf.images[image_index]
                    if image.uri:
                        if image.uri.startswith("data:"):
                            print(" - Found embedded base64 texture.")
                            header, encoded = image.uri.split(",", 1)
                            data = base64.b64decode(encoded)
                            print(f" - Embedded texture decoded (size: {len(data)} bytes)")
                        else:
                            print(f" - Texture image URI: {image.uri}")
                            
                    elif image.bufferView is not None:
                        print(" - Found embedded texture in bufferView.")
                        buffer_view = gltf.bufferViews[image.bufferView]
                        start = buffer_view.byteOffset or 0
                        end = start + (buffer_view.byteLength or 0)
                        image_data = glb_data[start:end]

                        print(f" - Embedded texture extracted (size: {len(image_data)} bytes)")
                    else:
                        print(" - No valid URI or bufferView found for image.")
                else:
                    print(" - No image found for this texture.")
            else:
                print(" - Texture index invalid or missing.")
        else:
            print(" - No baseColorTexture found.")

        if pbr.baseColorFactor:
            print(f" - baseColorFactor: {pbr.baseColorFactor}")
        else:
            print(" - No baseColorFactor found.")

        print("\n")