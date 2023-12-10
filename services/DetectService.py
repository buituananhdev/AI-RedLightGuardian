from ultralytics import YOLO

class YoloDetect:
    def __init__(self, model_type, detect_class=['car', 'motorcycle']):
        self.detect_class = detect_class
        self.model_type = model_type
        model_path = "../models/vehicle_detect/last.pt" if model_type == 1 else "../models/lisence_plate_detect/last.pt"
        self.model = YOLO(model_path)

    def process_box_info(self, box):
        x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
        conf = round(box.conf[0].item(), 2)
        class_id = self.model.names[box.cls[0].item()]

        return {"cords": [x1, y1, x2, y2], "class": class_id, "conf": conf}

    def detect(self, image, conf_threshold=0.1):
        arr_vehicle = []
        results = self.model.predict(image)
        
        for result in results:
            for box in result.boxes:
                conf = round(box.conf[0].item(), 2)
                
                if conf > conf_threshold:
                    box_info = self.process_box_info(box)

                    if self.model_type == 1:
                        arr_vehicle.append(box_info)
                    else:
                        return box_info

        return arr_vehicle
