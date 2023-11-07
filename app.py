import os
from flask import Flask, request, Response, json
import requests
from PIL import Image
from io import BytesIO
from flask_cors import CORS
from dotenv import load_dotenv
from services.DetectService import YoloDetect
from services.ProcessService import ProcessService
from helpers.helper import crop_image
from waitress import serve


app = Flask(__name__)
load_dotenv()
CORS(app)

EXTERNAL_API_URL = os.getenv("BUSINESS_SERVICE_URL")
WAITRESS_PORT = 3012

def get_image_from_request():
    if "image_file" not in request.files:
        return None, Response(
            json.dumps({"error": "Invalid request data"}),
            status=400,
            mimetype='application/json'
        )
    return request.files["image_file"], None

@app.route("/")
def root():
    """Handles the root endpoint, serves the HTML page."""
    with open("index.html") as file:
        return file.read()

@app.route("/detect", methods=["POST"])
def detect():
    image_file, error_response = get_image_from_request()
    if error_response:
        return error_response

    camera_coordinates = request.form.get("cords")
    try:
        cords = json.loads(camera_coordinates)
    except json.JSONDecodeError:
        return Response(
            json.dumps({"error": "Invalid cords data. Cannot parse JSON."}),
            status=400,
            mimetype='application/json'
        )

    process_service = ProcessService()
    list_license_plate = process_service.process_violation(Image.open(image_file.stream), cords)

    files = {'file': ('image.jpg', image_file, 'image/jpeg')}
    data = {'licensePlates': list_license_plate, 'cameraID': '1'}
    try:
        response = requests.post(EXTERNAL_API_URL + "violations", files=files, data=data)
        return Response(response.content, mimetype='application/json')
    except requests.RequestException as e:
        return Response(
            json.dumps({"error": f"Failed to make external API request: {str(e)}"}),
            status=500,
            mimetype='application/json'
        )

@app.route("/test", methods=["POST"])
def test():
    image_file, error_response = get_image_from_request()
    if error_response:
        return error_response

    model = YoloDetect(2)
    boxes = model.detect(Image.open(image_file.stream))

    if not boxes:
        return Response(
            json.dumps({"error": "No objects detected in the image"}),
            status=400,
            mimetype='application/json'
        )

    cropped_image = crop_image(image_file, boxes["cords"], '1')
    image_bytes = BytesIO()
    cropped_image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()

    files = {'file': ('image.jpg', image_bytes, 'image/jpeg')}

    try:
        response = requests.post('http://localhost:3011/api/storages/upload', files=files)
        if response.status_code == 200:
            return response.json(), 200
        else:
            return Response(
                json.dumps({"error": "Failed to upload image"}),
                status=500,
                mimetype='application/json'
            )
    except requests.RequestException as e:
        return Response(
            json.dumps({"error": f"Failed to upload image to external API: {str(e)}"}),
            status=500,
            mimetype='application/json'
        )

if __name__ == '__main__':
    print(f"Flask server is listening on port {WAITRESS_PORT}")
    serve(app, port=WAITRESS_PORT)
