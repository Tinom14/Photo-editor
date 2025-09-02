from PIL import Image, ImageFilter, ImageOps, ImageEnhance


def apply_filter(image: Image.Image, filter_data: dict) -> Image.Image:
    name = filter_data.get("name")
    params = filter_data.get("parameters", {})

    if name == "grayscale":
        return ImageOps.grayscale(image)
    if name == "blur":
        return image.filter(ImageFilter.GaussianBlur(radius=params.get("radius", 2)))
    if name == "sharpen":
        return image.filter(ImageFilter.SHARPEN)
    if name == "contour":
        return image.filter(ImageFilter.CONTOUR)
    if name == "brightness":
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(params.get("factor", 1.0))
    if name == "contrast":
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(params.get("factor", 1.0))
    if name == "saturation":
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(params.get("factor", 1.0))
    if name == "rotate":
        return image.rotate(params.get("angle", 0))
    if name == "edges":
        return image.filter(ImageFilter.FIND_EDGES)
    if name == "emboss":
        return image.filter(ImageFilter.EMBOSS)
    if name == "sepia":
        sepia_image = ImageOps.grayscale(image)
        sepia_image = ImageEnhance.Color(sepia_image).enhance(0.5)
        sepia_image = ImageEnhance.Contrast(sepia_image).enhance(0.8)
        return sepia_image
    if name == "invert":
        return ImageOps.invert(image)
    if name == "mirror":
        return ImageOps.mirror(image)
    if name == "flip":
        return ImageOps.flip(image)

    return image