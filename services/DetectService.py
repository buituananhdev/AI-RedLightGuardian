from ultralytics import YOLO

class YoloDetect():
    def __init__(self, model_type, detect_class=['car', 'motorcycle']):
        print('Loading model...')
        self.detect_class = detect_class
        self.model_type = model_type
        model_path = "../models/vehicle_detect/last.pt" if model_type == 1 else "../models/lisence_plate_detect/last.pt"
        self.model = YOLO(model_path)
        print('Model loaded!!')

    def detect(self, image):
        arr_vehicle = []
        results = self.model.predict(image)
        for result in results:
            for box in result.boxes:
                conf = round(box.conf[0].item(), 2)
                if conf > 0.1:
                    x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
                    class_id = result.names[box.cls[0].item()]
                    cords = box.xyxy[0].tolist()
                    cords = [round(x) for x in cords]
                    if self.model_type == 1:
                        arr_vehicle.append({"cords": [x1, y1, x2, y2], "class": class_id, "conf": conf})
                    else:
                        return {"cords": [x1, y1, x2, y2], "class": class_id, "conf": conf}
        return arr_vehicle

