import torch
import torchvision.transforms as transforms
from torchvision.transforms import ToPILImage as topil
import os
from PIL import Image
import uuid
from operation.net.detect_face import detect_faces
from operation.net.models import Generator as G
from operation.net.config import Config
from operation.net.utils import to_image

OUTPUT_PATH = 'operation/static/operation/images'


def generate_name():
    return str(uuid.uuid1()) + '.jpg'


def crop_image(image):
    boxes = detect_faces(image)
    pt1 = tuple(boxes[0][:2])
    pt1 = (int(pt1[0]), int(pt1[1]))
    pt2 = tuple(boxes[0][2:4])
    pt2 = (int(pt2[0]), int(pt2[1]))
    cropped = image.crop(pt1 + pt2)
    cropped_name = generate_name()
    cropped_path = os.path.join(OUTPUT_PATH, cropped_name)
    cropped.save(cropped_path)
    return cropped, pt1 + pt2, cropped_path


class Swapper(object):
    def __init__(self):
        self.config = Config()
        self.net = {
            'a2b': None,
            'b2a': None
        }
        self.net['a2b'] = G(self.config.in_channel, self.config.out_channel)
        self.net['a2b'].load_state_dict(torch.load('operation/net/checkpoints/ga2b.pth', map_location='cpu'))
        self.net['b2a'] = G(self.config.in_channel, self.config.out_channel)
        self.net['b2a'].load_state_dict(torch.load('operation/net/checkpoints/gb2a.pth', map_location='cpu'))

        transforms_ = [
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ]
        self.trans = transforms.Compose(transforms_)

    def swapgender(self, image_path, gender_model_name):
        img = Image.open(image_path)
        img = img.resize((256, int(img.size[1] / img.size[0] * 256)))
        _, _, crop_path = crop_image(img)

        '''
        crop, box, crop_path = crop_image(img)
        inputfile = self.trans(crop).unsqueeze(dim = 0)
        outcrop = topil()(to_image(self.net(inputfile).data.squeeze())).resize(crop.size)
        img = np.asarray(img)
        img = np.require(img, dtype='f4', requirements=['O', 'W'])
        img.flags.writeable = True
        outcrop = np.asarray(outcrop)
        img[box[1]:box[3], box[0]:box[2]] = outcrop
        img = Image.fromarray(np.uint8(img))
        '''
        img = self.trans(img).unsqueeze(dim=0)
        img = topil()(to_image(self.net[gender_model_name](img).data.squeeze()))

        name = generate_name()
        path = os.path.join(OUTPUT_PATH, name)
        img.save(path)

        return path, crop_path
