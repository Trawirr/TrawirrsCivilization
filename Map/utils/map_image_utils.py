from PIL import Image

def get_pixel_color(map_name: str, x: int, y: int) -> int:
    image_path = f"static/images/{map_name}_gray.png"
    image = Image.open(image_path)

    pixel_color = image.getpixel((x, y))

    return pixel_color