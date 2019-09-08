import torch
from torchvision.transforms import ToTensor
import os
from PIL import Image, ImageFont, ImageDraw
import uuid
from operation.net.cnn import CNN
from operation.net.detect_face import detect_faces

OUTPUT_PATH = 'operation/static/operation/images'
FONT = 'user/static/user/style/font/Gothic.ttf'

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)


def generate_name():
    return str(uuid.uuid1()) + '.jpg'


def crop_image(image):
    boxes = detect_faces(image)
    pt1 = tuple(boxes[0][:2])
    pt2 = tuple(boxes[0][2:4])
    cropped = image.crop(pt1 + pt2)
    # print('box', boxes, pt1 + pt2)
    cropped_name = generate_name()
    cropped_path = os.path.join(OUTPUT_PATH, cropped_name)
    cropped.save(cropped_path)
    return cropped_path


def draw(image, string):
    font_size = image.size[0] // 5
    font = ImageFont.truetype(FONT, font_size)
    draw_ = ImageDraw.Draw(image)
    x, y = 10, 10
    draw_.text((x, y), string, font=font)


class Detector:
    def __init__(self):
        self.fer = FaceEmotionRecognition()
        pass

    def __call__(self, image_path):
        raw_image = Image.open(image_path)
        cropped_path = crop_image(raw_image)
        recognition_path = self._recognition(raw_image)
        return recognition_path, cropped_path

    def _recognition(self, image):
        emotion = self.fer(image)
        draw(image, emotion)
        name = generate_name()
        path = os.path.join(OUTPUT_PATH, name)
        image.save(path)
        return path


class FaceEmotionRecognition:
    def __init__(self):
        self.net = CNN()
        checkpoint = torch.load('operation/static/models/CompactCNN_for_FER.t7', map_location='cpu')
        self.net.load_state_dict(checkpoint['net'])
        self.net.eval()

    def __call__(self, image):
        img = image.resize((96, 96), Image.ANTIALIAS)
        to_tensor = ToTensor()
        img = to_tensor(img)
        img = img.unsqueeze(0)
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
        return emotion
