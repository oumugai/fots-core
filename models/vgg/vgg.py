from torch import nn
from ...models.vgg.base import VGGBase
from ..layers import Conv2d
from collections import OrderedDict
"""
https://stackoverflow.com/questions/55140554/convolutional-encoder-error-runtimeerror-input-and-target-shapes-do-not-matc/55143487#55143487

Here is the formula;

N --> Input Size, F --> Filter Size, stride-> Stride Size, pdg-> Padding size

ConvTranspose2d;

OutputSize = N*stride + F - stride - pdg*2

Conv2d;

OutputSize = (N - F)/stride + 1 + pdg*2/stride [e.g. 32/3=10 it ignores after the comma]
"""


class VGGBase11_bn(VGGBase):
    def __init__(self, input_channels, **kwargs):
        Conv2d.batch_norm = True
        conv_layers = [
            *Conv2d.block_relumpool('1', 1, input_channels, 64),
        
            *Conv2d.block_relumpool('2', 1, 64, 128),

            *Conv2d.block_relumpool('3', 2, 128, 256),

            *Conv2d.block_relumpool('4', 2, 256, 512),

            *Conv2d.block_relumpool('5', 2, 512, 512),
        ]

        super().__init__(model_name='vgg11_bn', conv_layers=nn.ModuleDict(OrderedDict(conv_layers)), **kwargs)


class VGGBase11(VGGBase):
    def __init__(self, input_channels, **kwargs):
        Conv2d.batch_norm = False
        conv_layers = [
            *Conv2d.block_relumpool('1', 1, input_channels, 64),

            *Conv2d.block_relumpool('2', 1, 64, 128),

            *Conv2d.block_relumpool('3', 2, 128, 256),

            *Conv2d.block_relumpool('4', 2, 256, 512),

            *Conv2d.block_relumpool('5', 2, 512, 512)
        ]

        super().__init__(model_name='vgg11', conv_layers=nn.ModuleDict(OrderedDict(conv_layers)), **kwargs)

class VGGBase16_bn(VGGBase):
    def __init__(self, input_channels, **kwargs):
        Conv2d.batch_norm = True
        conv_layers = [
            *Conv2d.block_relumpool('1', 2, input_channels, 64),

            *Conv2d.block_relumpool('2', 2, 64, 128),

            *Conv2d.block_relumpool('3', 3, 128, 256),

            *Conv2d.block_relumpool('4', 3, 256, 512),

            *Conv2d.block_relumpool('5', 3, 512, 512),
        ]

        super().__init__(model_name='vgg16_bn', conv_layers=nn.ModuleDict(OrderedDict(conv_layers)), **kwargs)

class VGGBase16(VGGBase):
    def __init__(self, input_channels, **kwargs):
        Conv2d.batch_norm = False
        conv_layers = [
            *Conv2d.block_relumpool('1', 2, input_channels, 64),

            *Conv2d.block_relumpool('2', 2, 64, 128),

            *Conv2d.block_relumpool('3', 3, 128, 256),

            *Conv2d.block_relumpool('4', 3, 256, 512),

            *Conv2d.block_relumpool('5', 3, 512, 512),
        ]

        super().__init__(model_name='vgg16', conv_layers=nn.ModuleDict(OrderedDict(conv_layers)), **kwargs)

