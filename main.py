import os
from flask import request, Response, Flask
import requests
from waitress import serve
from PIL import Image
import json
from flask_cors import CORS
from services.ProcessService import ProcessService
from helpers.helper import draw_image_and_boxes, crop_image
from dotenv import load_dotenv
from io import BytesIO

app = Flask(__name__)
load_dotenv()
CORS(app)

external_api_url = os.getenv("BUSINESS_SERVICE_URL")

@app.route("/")
def root():
    """Handles the root endpoint, serves the HTML page."""
    with open("index.html") as file:
        return file.read()




if __name__ == '__main__':
    # Run the Flask app using Waitress server
    print("Flask server is listening on port 3012")
    serve(app, port=3012)
