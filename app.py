import os
from flask import Flask, request, Response, json, render_template
import requests
from PIL import Image
from io import BytesIO
from flask_cors import CORS
from dotenv import load_dotenv
from services.ProcessService import ProcessService
from helpers.helper import draw_image_and_boxes, get_image_from_request, get_cords
from waitress import serve
from services.CharacterService import CharacterDetect

app = Flask(__name__)
load_dotenv()
CORS(app)

EXTERNAL_API_URL = os.getenv("BUSINESS_SERVICE_URL")
WAITRESS_PORT = 3012
model = ProcessService()
test_model = CharacterDetect()
@app.route("/")
def root():
    """Handles the root endpoint, serves the HTML page."""
    return render_template('index.html', title='AI PBL4', name='Tuan Anh')

@app.route("/detect", methods=["POST"])
def detect():
    try:
        image_file, error_response = get_image_from_request()
        if error_response:
            return error_response

        cords = get_cords(EXTERNAL_API_URL + "cameras/2")
        result = model.process_violation(Image.open(BytesIO(image_file.read())), cords)
        print("Result of detect: ", result["list_license_plate_violation"])
        if(len(result) > 0):
            draw_image = draw_image_and_boxes(image_file, result["boxes"])
            files = {'file': ('image.jpg', draw_image, 'image/jpeg')}
            data = {'licensePlates': result["list_license_plate_violation"], 'cameraID': '1'}
            
            response = requests.post(EXTERNAL_API_URL + "violations", files=files, data=data)
            return Response(response.content, mimetype='application/json')
        else:
            return Response("No vehicle found", mimetype='application/json')
        
    except Exception as e:
        return Response(
            json.dumps(str(e)),
            status=500,
            mimetype='application/json'
        )


@app.route("/test", methods=["POST"])
def test():
    image_file, error_response = get_image_from_request()
    if error_response:
        return error_response

    result = test_model.detect(Image.open(BytesIO(image_file.read())))
    return Response(
            json.dumps(result),
            status=200,
            mimetype='application/json'
        )


if __name__ == '__main__':
    print(f"Flask server is listening on port {WAITRESS_PORT}")
    serve(app, port=WAITRESS_PORT)
