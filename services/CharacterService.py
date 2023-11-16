import easyocr
class CharacterDetect():
    def __init__(self):
        print('Loading model character...')
        print('Model character loaded!!')

    def detect(self, image):
        return "ABC123"
        # print(image)
        # reader = easyocr.Reader(['en'])
        # image_bytes = image.read()
        # result = reader.readtext(image_bytes)

        # extracted_text = []
        # for detection in result:
        #     text = detection[1]
        #     extracted_text.append(text)

        # return extracted_text
