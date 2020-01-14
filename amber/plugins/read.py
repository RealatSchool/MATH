import requests
from io import BytesIO
import importlib

class ReadSession:


    def __init__(self, client, config):
        self.client = client
        self.config = config
        importlib.import_module("tools.ocr", self)
	
	
    async def respond(self, message):
        response = "The image(s) say: ```"
        count = 0
        for image in message.attachments:
            for extension in self.config["file_types"]:
                if image["url"].endswith(extension):
                    count += 1
                    #get the url from the message attachment, send it to bytes io and then open it as an image. Then, send to OCRTool
                    response = response + "``` - Image " + str(count) + "\n\n" + ocr.OCRTool.readImage(Image.open(BytesIO(requests.get(image["url"]).content)))
        response = response.replace("*", "\*")
        
        await self.client.send(response, message.channel)

def load(client, config):
    return ReadSession(client, config)
