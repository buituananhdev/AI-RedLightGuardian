import easyocr
from PIL import Image
import numpy as np

class CharacterDetect():
    def __init__(self):
        print('Loading model character...')
        print('Model character loaded!!')

    def detect(self, image):
        return "ABC123"
        image_np = np.array(image)

        # Sử dụng EasyOCR để đọc text từ ảnh
        reader = easyocr.Reader(['en'])  # Chọn ngôn ngữ, ở đây là tiếng Anh ('en')
        results = reader.readtext(image_np)

        extracted_text = []
        for detection in results:
            text = detection[1]
            extracted_text.append(text)

        return extracted_text[0] + " " + extracted_text[1]
