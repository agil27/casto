import torch
from torchvision.transforms import ToTensor
from operation.net.cnn import CNN
import os
from PIL import Image, ImageFont, ImageDraw
import uuid


OUTPUT_PATH = 'operation/static/operation/images'
FONT = 'user/static/user/style/font/Gothic.ttf'

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)


class CompactCNN:
    def __init__(self):
        self.net = CNN()
        print('loading model...')
        checkpoint = torch.load('operation/static/models/CompactCNN_for_FER.t7')
        self.net.load_state_dict(checkpoint['net'])
        self.net.eval()

    def __call__(self, image_path):
        print('loading image...')
        raw_img = Image.open(image_path)
        origin_size = raw_img.size
        raw_img = raw_img.resize((96, 96), Image.ANTIALIAS)
        to_tensor = ToTensor()
        img = to_tensor(raw_img)
        img = img.unsqueeze(0)
        print('forward...')
        out = self.net(img)
        cls = out.argmax(1).item()
        cls2emotion = {
            0: 'anger',
            1: 'contempt',
            2: 'disgust',
            3: 'fear',
            4: 'happy',
            5: 'sadness',
            6: 'surprise'
        }
        emotion = cls2emotion[cls]
        print('drawing...')
        raw_img = raw_img.resize(origin_size, Image.ANTIALIAS)
        self._draw(raw_img, emotion)
        name = str(uuid.uuid1()) + '.jpg'
        path = os.path.join(OUTPUT_PATH, name)
        raw_img.save(path)
        return path

    @staticmethod
    def _draw(image, string):
        font = ImageFont.truetype(FONT, 20)
        draw = ImageDraw.Draw(image)
        x, y = 10, 10
        draw.text((x, y), string, font=font)

