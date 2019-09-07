import torch
from torchvision.transforms import ToTensor
import os
from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np
import uuid
from casto.settings import BASE_DIR
from operation.net.cnn import CNN


OUTPUT_PATH = 'operation/static/operation/images'
FONT = 'user/static/user/style/font/Gothic.ttf'
OPENCV_PATH = 'operation/static/opencv/haarcascades_frontalface_default.xml'

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)


'''
class Detector:
    def __init__(self):
        # self.compactCNN = CompactCNN()
        pass

    def __call__(self, image_path):
        raw_image = cv2.imread(image_path)
        gray = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
        path = os.path.join(BASE_DIR, OPENCV_PATH)
        path = path.replace('/', os.sep)
        print(r''.format(path))
        face_cascade = cv2.CascadeClassifier(r''.format(path))
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.15,
            minNeighbors=3,
            minSize=(5, 5)
        )
        for x, y, w, h in faces:
            pass
'''


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
        raw_img = Image.open(image_path)
        self._draw(raw_img, emotion)
        name = str(uuid.uuid1()) + '.jpg'
        path = os.path.join(OUTPUT_PATH, name)
        raw_img.save(path)
        return path

    @staticmethod
    def _draw(image, string):
        font_size = image.size[0] // 5
        font = ImageFont.truetype(FONT, font_size)
        draw = ImageDraw.Draw(image)
        x, y = 10, 10
        draw.text((x, y), string, font=font)

