from helpers.helper import is_center_inside_rectangle, convert_to_coordinates, crop_image
from services.DetectService import YoloDetect
from services.CharacterService import CharacterDetect

class ProcessService():
    def __init__(self):
        self.vehicle_model = YoloDetect(1)
        self.license_plate_model = YoloDetect(2)
        self.character_model = CharacterDetect()

    def detect_vehicles_violation(self, image, camera_coordinates):
        results = self.vehicle_model.detect(image)
        camera_rectangle = camera_coordinates
        return [obj for obj in results if not is_center_inside_rectangle(obj["cords"], convert_to_coordinates(camera_rectangle))]

    def detect_license_plate(self, image):
        result = self.character_model.detect(image)
        return result

    def process_violation(self, image, camera_coordinates):
        list_license_plate_violation = []
        list_vehicles = self.detect_vehicles_violation(image, camera_coordinates)
        print("list_vehicles", list_vehicles)
        for vehicle in list_vehicles:
            vehicle_img = crop_image(image, vehicle["cords"])
            license_plate = self.license_plate_model.detect(vehicle_img)
            if license_plate:
                license_plate_img = crop_image(
                    vehicle_img, license_plate['cords'])
                license_plate_text = self.detect_license_plate(license_plate_img)
                list_license_plate_violation.append(license_plate_text)

        return {'list_license_plate_violation': list_license_plate_violation, 'boxes': list_vehicles}
