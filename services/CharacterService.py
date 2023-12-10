import easyocr
import numpy as np
import cv2
from helpers.helper import format_license_plate
class CharacterDetect:
    def __init__(self):
        # Initialize EasyOCR reader only once
        self.reader = easyocr.Reader(['en'])

    def detect(self, image):
        # Convert PIL Image to NumPy array
        image_np = np.array(image)

        # Convert to grayscale
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

        # Apply bilateral filter
        gray_image = cv2.bilateralFilter(gray_image, d=9, sigmaColor=75, sigmaSpace=75)

        # Use EasyOCR to read text from the image
        results = self.reader.readtext(gray_image)

        extracted_text = [detection[1] for detection in results]

        return format_license_plate(extracted_text)
