from helpers.helper import is_center_inside_rectangle, convert_to_coordinates, crop_image, draw_image_and_boxes
from services.DetectService import YoloDetect
from services.CharacterService import CharacterDetect


class ProcessService():
    def __init__(self):
        # Khởi tạo đối tượng YoloDetect để nhận diện phương tiện và biển số xe
        self.vehicle_model = YoloDetect(1)  # Đối tượng nhận diện phương tiện
        self.license_plate_model = YoloDetect(2)  # Đối tượng nhận diện biển số xe
        self.character_model = CharacterDetect()

    def detect_vehicles_violation(self, image, camera_coordinates):
        # Nhận diện các phương tiện vi phạm trong hình ảnh
        results = self.vehicle_model.detect(image)
        # Chuyển đổi tọa độ của camera thành hình chữ nhật
        # Assuming convert_to_coordinates is not needed and using camera_coordinates directly
        camera_rectangle = camera_coordinates
        # Lọc các phương tiện không nằm trong vùng camera quy định
        return [obj for obj in results if not is_center_inside_rectangle(obj["cords"], convert_to_coordinates(camera_rectangle))]

    def detect_license_plate(self, image):
        result = self.character_model.detect(image)
        return result

    def process_violation(self, image, camera_coordinates):
        list_license_plate_violation = []
        # Nhận diện các phương tiện vi phạm trong hình ảnh
        list_vehicles = self.detect_vehicles_violation(image, camera_coordinates)
        print("list_vehicles", list_vehicles)
        # Xử lý vi phạm cho từng phương tiện được nhận diện
        for vehicle in list_vehicles:
            # Cắt ảnh của phương tiện từ hình ảnh gốc
            vehicle_img = crop_image(image, vehicle["cords"])
            # Nhận diện biển số xe trên ảnh của phương tiện
            license_plate = self.license_plate_model.detect(vehicle_img)
            print("License Plate:", license_plate)
            # Cắt ảnh của biển số xe từ ảnh của phương tiện
            if license_plate:
                license_plate_img = crop_image(
                    vehicle_img, license_plate['cords'])
                # Nhận diện chữ số trên biển số xe
                license_plate_text = self.detect_license_plate(
                    license_plate_img)
                # Thêm biển số xe vi phạm vào danh sách kết quả
                list_license_plate_violation.append(license_plate_text)

        # Trả về danh sách các biển số xe vi phạm
        return {'list_license_plate_violation': list_license_plate_violation, 'boxes': list_vehicles}
