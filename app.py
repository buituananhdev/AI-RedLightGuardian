from flask import request, Response, Flask
from waitress import serve
from PIL import Image
import json
from flask_cors import CORS
from services.DetectService import YoloDetect

app = Flask(__name__)


@app.route("/")
def root():
    with open("index.html") as file:
        return file.read()


@app.route("/detect", methods=["POST"])
def detect():
    print(request.form)
    if "image_file" not in request.files or "cords" not in request.form:
        return Response(
            json.dumps({"error": "Invalid request data"}),
            status=400,
            mimetype='application/json'
        )

    buf = request.files["image_file"]
    cords_str = request.form["cords"]
    
    try:
        cords = json.loads(cords_str)
    except json.JSONDecodeError:
        return Response(
            json.dumps({"error": "Invalid cords data. Cannot parse JSON."}),
            status=400,
            mimetype='application/json'
        )

    boxes = detect_objects_on_image(Image.open(buf.stream), cords)
    return Response(
        json.dumps(boxes),
        mimetype='application/json'
    )


def detect_objects_on_image(buf, cords):
    model = YoloDetect()
    result = model.check_violations(buf, cords)
    return {'count': len(result), 'data': result}


CORS(app)

if __name__ == '__main__':
    print("Flask server is listening on port 8080")
    serve(app, port=3012)
