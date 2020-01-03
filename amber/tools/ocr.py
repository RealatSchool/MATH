import pytesseract

class OCRTool:

    def __init__(self, config):
        self.config = config
        if self.config["tools"]["ocr"]['tesseract_path'] != "":
            pytesseract.pytesseract.tesseract_cmd = self.config["tools"]["ocr"]['tesseract_path']

    #takes PIL image as input
    def readImage(self, image):
        return pytesseract.image_to_string(image)
