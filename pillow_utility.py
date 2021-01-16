from PIL import Image, ImageDraw, ImageFont

def draw_boundary(image, bounding, color, image_size, caption='', confidence_score=0):
    width, height = image_size
    draw = ImageDraw.Draw(image)
    draw.polygon([
        bounding.normalized_vertices[0].x *
        width, bounding.normalized_vertices[0].y * height,
        bounding.normalized_vertices[1].x *
        width, bounding.normalized_vertices[1].y * height,
        bounding.normalized_vertices[2].x *
        width, bounding.normalized_vertices[2].y * height,
        bounding.normalized_vertices[3].x * width, bounding.normalized_vertices[3].y * height], fill=None, outline=color)

    font_size = width * height // 22000 if width * height > 400000 else 12

    font = ImageFont.truetype(r'C:/Windows/Fonts/Arial.ttf', 22)

    draw.text((bounding.normalized_vertices[0].x * width, bounding.normalized_vertices[0].y * height), font=font, text=caption, fill=color)

    draw.text((bounding.normalized_vertices[0].x * width, bounding.normalized_vertices[0].y * height + 20), font=font, text='Confidence: {}'.format(confidence_score), fill=color)

    return image
