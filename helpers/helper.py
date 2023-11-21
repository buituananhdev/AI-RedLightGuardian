from PIL import Image, ImageDraw
import io
from flask import request, Response, json

def is_center_inside_rectangle(rectangle1, rectangle2):
    center_x1 = (rectangle1[0] + rectangle1[2]) / 2
    center_y1 = (rectangle1[1] + rectangle1[3]) / 2

    x2, y2, x3, y3 = rectangle2
    if x2 < center_x1 < x3 and y2 < center_y1 < y3:
        return True
    else:
        return False


def convert_to_coordinates(points):
    x_values = [point["x"] for point in points]
    y_values = [point["y"] for point in points]

    xmin = min(x_values)
    ymin = min(y_values)
    xmax = max(x_values)
    ymax = max(y_values)

    coordinates = [xmin, ymin, xmax, ymax]
    return coordinates

def draw_image_and_boxes(image_file, boxes):
    """Draw bounding boxes on the image and return the modified image."""
    # Open the image and create a copy
    img = Image.open(image_file.stream).copy()

    # Convert the image to RGBA mode for a wider color range
    img = img.convert("RGBA")
    draw = ImageDraw.Draw(img)

    for box in boxes:
        x1, y1, x2, y2 = box["cords"]
        label = box["class"]
        probability = box["conf"]

        # Draw bounding box with RGBA color
        draw.rectangle([x1, y1, x2, y2], outline=(0, 255, 0, 255), width=3)

        # Draw filled rectangle for label background
        draw.rectangle([x1, y1, x1 + len(f"{label} ({probability})") * 8, y1 + 25], fill=(0, 255, 0, 128))

        # Draw text on the image
        draw.text((x1, y1 + 18), f"{label} ({probability})", fill=(0, 0, 0, 255))

    # Save the modified image as bytes and return
    img = img.convert("RGB")  # Convert back to RGB mode before saving
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


def crop_image(image, coordinates):
    left, upper, right, lower = coordinates
    cropped_image = image.crop((left, upper, right, lower))
    return cropped_image

def get_image_from_request():
    if "image_file" not in request.files:
        return None, Response(
            json.dumps({"error": "Invalid request data"}),
            status=400,
            mimetype='application/json'
        )
    return request.files["image_file"], None