import os
from flask import request, Response, Flask
import requests
from waitress import serve
from PIL import Image, ImageDraw
import io
import json
from flask_cors import CORS
from services.DetectService import YoloDetect
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
CORS(app)

@app.route("/")
def root():
    """Handles the root endpoint, serves the HTML page."""
    with open("index.html") as file:
        return file.read()

@app.route("/detect", methods=["POST"])
def detect():
    """Endpoint to process image detection and call external API."""
    # Check if required data is present in the request
    if "image_file" not in request.files or "cords" not in request.form:
        return Response(
            json.dumps({"error": "Invalid request data"}),
            status=400,
            mimetype='application/json'
        )

    # Get image file and coordinates from the request
    image_file = request.files["image_file"]
    cords_str = request.form["cords"]

    try:
        cords = json.loads(cords_str)
    except json.JSONDecodeError:
        return Response(
            json.dumps({"error": "Invalid cords data. Cannot parse JSON."}),
            status=400,
            mimetype='application/json'
        )

    # Detect objects in the image
    boxes = detect_objects_on_image(Image.open(image_file.stream), cords)

    # Draw bounding boxes on the image and prepare the response
    draw_image = draw_image_and_boxes(image_file, boxes)
    files = {'file': ('image.jpg', draw_image, 'image/jpeg')}
    data = {'licensePlate': 'ABC123', 'cameraID': '1'}
    response = call_external_api(files, data)

    return Response(
        json.dumps(response),
        mimetype='application/json'
    )

def detect_objects_on_image(image, cords):
    """Detect objects in the given image using YOLO model."""
    model = YoloDetect()
    result = model.check_violations(image, cords)
    return result

def draw_image_and_boxes(image_file, boxes):
    """Draw bounding boxes on the image and return the modified image."""
    img = Image.open(image_file.stream).copy()
    draw = ImageDraw.Draw(img)

    for box in boxes:
        print(box)
        x1, y1, x2, y2, label, probability = box
        draw.rectangle([x1, y1, x2, y2], outline="#00FF00", width=3)
        text = f"{label} ({probability})"
        draw.rectangle([x1, y1, x1 + len(text) * 8, y1 + 25], fill="#00ff00")  # Adjust the width based on the text length
        draw.text((x1, y1 + 18), text, fill="#000000")

    # Save the modified image as bytes and return
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def call_external_api(files, data):
    """Call an external API with files and data, and return the response."""
    external_api_url = os.getenv("BUSINESS_SERVICE_URL")
    response = requests.post(external_api_url, files=files, data=data)
    
    return response.json()


if __name__ == '__main__':
    # Run the Flask app using Waitress server
    print("Flask server is listening on port 8080")
    serve(app, port=3012)
