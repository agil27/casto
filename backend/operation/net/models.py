import torch
import torch.nn as nn
import torch.nn.functional as F

##### Residue Block #####
class ResBlock(nn.Module):
    def __init__(self, in_features):
        super(ResBlock, self).__init__()

        self.conv = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.InstanceNorm2d(in_features),
            nn.ReLU(inplace = True),
            nn.ReflectionPad2d(1),
            nn.Conv2d(in_features, in_features, 3),
            nn.InstanceNorm2d(in_features)
        )
    
    def forward(self, x):
        return x + self.conv(x)

##### GAN #####
class Generator(nn.Module):
    def __init__(self, in_channel, out_channel, num_resblocks = 9):
        super(Generator, self).__init__()

        # Initial convolution block
        self.init = nn.Sequential(
            nn.ReflectionPad2d(3),
            nn.Conv2d(in_channel, 64, 7),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace = True)
        )

        # Down Sampling
        self.ds1 = nn.Sequential(
            nn.Conv2d(64, 128, 3, stride = 2, padding = 1),
            nn.InstanceNorm2d(128),
            nn.ReLU(inplace = True)
        )
        
        self.ds2 = nn.Sequential(
            nn.Conv2d(128, 256, 3, stride = 2, padding = 1),
            nn.InstanceNorm2d(256),
            nn.ReLU(inplace = True)
        )

        # Residual Blocks
        self.res = nn.Sequential(
            ResBlock(128),
            ResBlock(128)
        )

        # Up Sampling
        self.us1 = nn.Sequential(
            nn.ConvTranspose2d(256, 128, 3, stride = 2, padding = 1, output_padding = 1),
            nn.InstanceNorm2d(128),
            nn.ReLU(inplace = True)
        )

        self.us2 = nn.Sequential(
            nn.ConvTranspose2d(128, 64, 3, stride = 2, padding = 1, output_padding = 1),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace = True)
        )

        # Output Layer
        self.output = nn.Sequential(
            nn.ReflectionPad2d(3),
            nn.Conv2d(64, out_channel, 7),
            nn.Tanh()
        )

    def forward(self, x):
        x = self.init(x)
        x = self.ds1(x)
        x = self.ds2(x)
        x = self.us1(x)
        x = self.us2(x)
        x = self.output(x)
        return x

class Discriminator(nn.Module):
    def __init__(self, in_channel):
        super(Discriminator, self).__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channel, 64, 4, stride = 2, padding = 1),
            nn.LeakyReLU(0.2, inplace = True)
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(64, 128, 4, stride = 2, padding = 1),
            nn.InstanceNorm2d(128),
            nn.LeakyReLU(0.2, inplace = True)
        )

        self.conv3 = nn.Sequential(
            nn.Conv2d(128, 256, 4, stride = 2, padding = 1),
            nn.InstanceNorm2d(256),
            nn.LeakyReLU(0.2, inplace = True)
        )

        self.conv4 = nn.Sequential(
            nn.Conv2d(256, 512, 4, stride = 2, padding = 1),
            nn.InstanceNorm2d(512),
            nn.LeakyReLU(0.2, inplace = True)
        )

        self.fc = nn.Conv2d(512, 1, 4, padding = 1)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.fc(x)
        x = F.avg_pool2d(x, x.size()[2:]).view(x.size()[0], -1)
        return x

##### Compact CNN for Facial Expression Classifying #####
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=16, kernel_size=5, stride=1, padding=2),
            nn.PReLU(),
            nn.Conv2d(in_channels=16, out_channels=16, kernel_size=5, stride=1, padding=2),
            nn.PReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=1, padding=2),
            nn.PReLU(),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, stride=1, padding=2),
            nn.PReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc1 = nn.Linear(32 * 24 * 24, 32 * 24 * 24)
        self.fc2 = nn.Linear(32 * 24 * 24, 7)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.fc1(x)
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.fc2(x)
        return x