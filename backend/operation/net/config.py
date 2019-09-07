import warnings
import torch

class Config(object):
    init_epoch = 0
    num_epochs = 40
    batch_size = 1
    data_root = 'dataset/male2female/'
    model_addr = 'saved_models/'
    output_root = 'm2f_output/'
    lr = 0.0002
    decay_epoch = 20
    size = 256
    in_channel = 3
    out_channel = 3
    cuda = torch.cuda.is_available()
    num_cpu = 8
    def parse(self, kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                warnings.warn("Warning: opt has not attribute %s" % key)
            else:
                setattr(self, key, value)