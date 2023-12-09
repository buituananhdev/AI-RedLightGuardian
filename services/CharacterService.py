import easyocr
from PIL import Image
import numpy as np
import cv2
def format_license_plate(extracted_text):
    full_text = ''.join(extracted_text)
    if len(full_text) == 8 and full_text[:2].isdigit() and full_text[2].isalpha() and full_text[3:].isdigit():
        return full_text

    formatted_text = ''
    if len(extracted_text) == 2: 
        if(len(extracted_text[0]) == 3): 
            formatted_text = extracted_text[0] + extracted_text[1]
        else:
            formatted_text = extracted_text[1] + extracted_text[0]
    return formatted_text
class CharacterDetect:
    def __init__(self):
        print('Loading model character...')
        # Initialize EasyOCR reader only once
        self.reader = easyocr.Reader(['en'])
        print('Model character loaded!!')

    def detect(self, image):
        # Convert PIL Image to NumPy array
        image.save("test.png")
        image_np = np.array(image)
        # Convert to grayscale
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("gray_image.png", gray_image)

        # Apply bilateral filter
        gray_image = cv2.bilateralFilter(gray_image, d = 9, sigmaColor = 75, sigmaSpace = 75)
        # Use EasyOCR to read text from the image
        results = self.reader.readtext(gray_image, decoder='beamsearch', beamWidth=10, contrast_ths=0.1, adjust_contrast=0.5, filter_ths=0.5)

        extracted_text = [detection[1] for detection in results]
        print('extracted_text', extracted_text)

        return format_license_plate(extracted_text)
