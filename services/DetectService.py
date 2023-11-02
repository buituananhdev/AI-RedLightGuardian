import os
from ultralytics import YOLO


def is_center_inside_rectangle(obj, rectangle2):
    rectangle1 = [int(obj[0]), int(obj[1]), int(obj[2]), int(obj[3])]
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


class YoloDetect():
    def __init__(self, detect_class=['car', 'motorcycle']):
        print('Loading model...')
        self.detect_class = detect_class
        # Lấy đường dẫn đến thư mục hiện tại của file .py
        current_directory = os.path.dirname(os.path.abspath(__file__))
        modal_path = os.path.join(
            current_directory, 'modals', 'yolov8s', 'last.pt')
        self.modal = YOLO(modal_path)
        print('Model loaded!!')

    def detect(self, image):
        arr = []
        results = self.modal.predict(image)
        for result in results:
            for box in result.boxes:
                conf = round(box.conf[0].item(), 2)
                if conf > 0.4:
                    x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
                    class_id = result.names[box.cls[0].item()]
                    cords = box.xyxy[0].tolist()
                    cords = [round(x) for x in cords]
                    arr.append([x1, y1, x2, y2, class_id, conf])
        return arr

    def check_violations(self, image, camera_coordinates):
        results = self.detect(image)
        list_vehicle_violation = []
        camera_rectangle = convert_to_coordinates(camera_coordinates)
        for obj in results:
            if not is_center_inside_rectangle(obj, camera_rectangle):
                list_vehicle_violation.append(obj)
        return list_vehicle_violation
