import numpy as np

from ..objrecog.target_transforms import (
    Compose,
    OneHot,
    ToTensor
)
from .._utils import _check_ins
from ..base.exceptions import _TargetTransformBaseException

class Text2Number(object):
    class NotContainError(_TargetTransformBaseException):
        pass

    def __init__(self, class_labels, blankIndex=None, ignore_nolabel=True, toLower=True):
        self._class_labels = class_labels

        blankIndex = _check_ins('blankIndex', blankIndex, int, allow_none=True)
        if blankIndex:
            self._class_labels.insert(blankIndex, '-')

        self._ignore_nolabel = ignore_nolabel
        self._toLower = toLower

    def __call__(self, labels, *args):
        ret_labels = []
        drop_words = []
        for c in labels:
            try:
                c = c.lower() if self._toLower else c
                if c in self._class_labels:
                    ret_labels += [self._class_labels.index(c)]
                else:
                    drop_words.append(c)
            except ValueError:
                if self._ignore_nolabel:
                    continue
                else:
                    raise Text2Number.NotContainError('{} didn\'t contain ({})'.format(labels, ''.join(self._class_labels)))
                    
        if len(drop_words) > 0:
            #print(drop_words)
            with open("./gdrive/My Drive/FOTS/not_used_word.txt", "a") as file:
                file.write(" ".join(drop_words))
        return (np.array(ret_labels), *args)
