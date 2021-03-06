import os, logging, re, shutil, sys, csv
from scipy import io as sio
from lxml import etree
import cv2
import numpy as np

class _Skip(Exception):
    pass

def VOCGenerator(basedir, imagedirname='SynthText', skip_missing=False, encoding='utf-8'):

    def xmlgenerator(annodir, imagedir, cbb, wBB, imname, txts, **kwargs):
        imgpath = os.path.join(imagedir, imname)

        if not os.path.exists(imgpath):
            if not skip_missing:
                raise FileNotFoundError('{} was not found'.format(imgpath))
            else:
                logging.warning('Missing image: {}'.format(imgpath))
                raise _Skip()

        root = etree.Element('annotation')

        # folder
        folderET = etree.SubElement(root, 'folder')
        folder = os.path.dirname(imname)
        folderET.text = folder
        # filename
        filenameET = etree.SubElement(root, 'filename')
        filename = os.path.basename(imname)
        filenameET.text = filename

        # read image to get height, width, channel
        img = cv2.imread(imgpath)
        h, w, c = img.shape

        # size
        sizeET = etree.SubElement(root, 'size')

        # width
        widthET = etree.SubElement(sizeET, 'width')
        widthET.text = str(w)
        # height
        heightET = etree.SubElement(sizeET, 'height')
        heightET.text = str(h)
        # depth
        depthET = etree.SubElement(sizeET, 'depth')
        depthET.text = str(c)

        # convert txts to list of str
        # I don't know why texts is
        # ['Lines:\nI lost\nKevin ', 'will                ', 'line\nand            ',
        # 'and\nthe             ', '(and                ', 'the\nout             ',
        # 'you                 ', "don't\n pkg          "]
        # there is strange blank and the length of txts is different from the one of wBB
        txts = ' '.join(txts.tolist()).split()
        text_num = len(txts)

        if wBB.ndim == 2:
            # convert shape=(2, 4,) to (2, 4, 1)
            wBB = np.expand_dims(wBB, 2)

        assert text_num == wBB.shape[2], 'The length of text and wordBB must be same, but got {} and {}'.format(
            text_num, wBB.shape[2])
        for b in range(text_num):
            # object
            objectET = etree.SubElement(root, 'object')

            # difficult
            difficultET = etree.SubElement(objectET, 'difficult')
            difficultET.text = '0'
            # content
            contentET = etree.SubElement(objectET, 'content')
            contentET.text = '###'
            # name
            nameET = etree.SubElement(objectET, 'name')
            nameET.text = txts[b]
            # bndbox
            bndboxET = etree.SubElement(objectET, 'bndbox')

            # quad
            for q in range(4):
                xET = etree.SubElement(bndboxET, 'x{}'.format(q + 1))
                xET.text = str(wBB[0, q, b])
                yET = etree.SubElement(bndboxET, 'y{}'.format(q + 1))
                yET.text = str(wBB[1, q, b])

            # corner
            xminET = etree.SubElement(bndboxET, 'xmin')
            xminET.text = str(np.min(wBB[0, :, b]))
            yminET = etree.SubElement(bndboxET, 'ymin')
            yminET.text = str(np.min(wBB[1, :, b]))
            xmaxET = etree.SubElement(bndboxET, 'xmax')
            xmaxET.text = str(np.max(wBB[0, :, b]))
            ymaxET = etree.SubElement(bndboxET, 'ymax')
            ymaxET.text = str(np.max(wBB[1, :, b]))

        xmlstr = etree.tostring(root, pretty_print=True, encoding=encoding)
        dstpath = os.path.join(annodir, folder, os.path.splitext(filename)[0] + '.xml')

        if not os.path.isdir(os.path.dirname(dstpath)):
            os.mkdir(os.path.dirname(dstpath))

        with open(dstpath, 'wb') as f:
            f.write(xmlstr)

    _gtmatRecognizer(xmlgenerator, basedir, imagedirname)

def TextRecogCSVGenerator(basedir, imagedirname='SynthText', skip_missing=False, encoding='utf-8'):

    lines = [['folder', 'filename', 'text', 'xmin', 'ymin', 'xmax', 'ymax',
             'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']]

    def csvgenerator(annodir, imagedir, cbb, wBB, imname, txts, **kwargs):
        lines = kwargs.get('lines')

        imgpath = os.path.join(imagedir, imname)

        if not os.path.exists(imgpath):
            if not skip_missing:
                raise FileNotFoundError('{} was not found'.format(imgpath))
            else:
                logging.warning('Missing image: {}'.format(imgpath))
                raise _Skip()

        folder = os.path.dirname(imname)
        filename = os.path.basename(imname)

        # convert txts to list of str
        # I don't know why txts is
        # ['Lines:\nI lost\nKevin ', 'will                ', 'line\nand            ',
        # 'and\nthe             ', '(and                ', 'the\nout             ',
        # 'you                 ', "don't\n pkg          "]
        # there is strange blank and the length of txts is different from the one of wBB
        txts = ' '.join(txts.tolist()).split()
        text_num = len(txts)

        if wBB.ndim == 2:
            # convert shape=(2, 4,) to (2, 4, 1)
            wBB = np.expand_dims(wBB, 2)

        assert text_num == wBB.shape[2], 'The length of text and wordBB must be same, but got {} and {}'.format(
            text_num, wBB.shape[2])
        for b in range(text_num):
            text = txts[b]

            # quad
            quad = []
            for q in range(4):
                quad += [str(wBB[0, q, b]), str(wBB[1, q, b])]

            # corner
            corner = [str(np.min(wBB[0, :, b])), str(np.min(wBB[1, :, b])),
                      str(np.max(wBB[0, :, b])), str(np.max(wBB[1, :, b]))]

            lines += [[folder, filename, text, *corner, *quad]]

    _gtmatRecognizer(csvgenerator, basedir, imagedirname, lines=lines)

    annodir = os.path.join(basedir, 'Annotations')
    with open(os.path.join(annodir, 'gt.csv'), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(lines)

def TextRecogOnlyAlphabetNumberCSVGenerator(basedir, imagedirname='SynthText', skip_missing=False, encoding='utf-8'):

    lines = [['folder', 'filename', 'text', 'xmin', 'ymin', 'xmax', 'ymax',
             'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']]

    def csvgenerator(annodir, imagedir, cbb, wBB, imname, txts, **kwargs):
        lines = kwargs.get('lines')

        imgpath = os.path.join(imagedir, imname)

        img = cv2.imread(imgpath)
        h, w, _ = img.shape
        if not os.path.exists(imgpath):
            if not skip_missing:
                raise FileNotFoundError('{} was not found'.format(imgpath))
            else:
                logging.warning('Missing image: {}'.format(imgpath))
                raise _Skip()

        folder = os.path.dirname(imname)
        filename = os.path.basename(imname)

        # convert txts to list of str
        # I don't know why txts is
        # ['Lines:\nI lost\nKevin ', 'will                ', 'line\nand            ',
        # 'and\nthe             ', '(and                ', 'the\nout             ',
        # 'you                 ', "don't\n pkg          "]
        # there is strange blank and the length of txts is different from the one of wBB
        txts = ' '.join(txts.tolist()).split()
        text_num = len(txts)

        if wBB.ndim == 2:
            # convert shape=(2, 4,) to (2, 4, 1)
            wBB = np.expand_dims(wBB, 2)

        assert text_num == wBB.shape[2], 'The length of text and wordBB must be same, but got {} and {}'.format(
            text_num, wBB.shape[2])

        charind = 0
        # replace non-alphanumeric characters with *
        alltexts_asterisk = ''.join([re.sub(r'[^A-Za-z0-9]', '*', text) for text in txts])
        assert len(alltexts_asterisk) == cbb.shape[2], 'The length of characters and cbb must be same, but got {} and {}'.format(
            len(alltexts_asterisk), cbb.shape[2])
        for b in range(text_num):
            text = txts[b]

            alphanumerictext = re.findall(r'[A-Za-z0-9]+', text)

            for ant in alphanumerictext:
                charind = alltexts_asterisk.index(ant, charind)

                # quad
                quad = [cbb[0, 0, charind], cbb[1, 0, charind], # top-left
                        cbb[0, 1, charind+len(ant)-1], cbb[1, 1, charind+len(ant)-1],
                        cbb[0, 2, charind+len(ant)-1], cbb[1, 2, charind+len(ant)-1],
                        cbb[0, 3, charind], cbb[1, 3, charind]]

                # corner
                xmin, ymin, xmax, ymax = max(np.min(quad[0::2]), 0), max(np.min(quad[1::2]), 0), min(np.max(quad[0::2]), w), min(np.max(quad[1::2]), h)
                _h, _w, _ = img[int(ymin):int(ymax), int(xmin):int(xmax)].shape
                if _h == 0 or _w == 0:
                    charind += len(ant)
                    continue
                corner = [xmin, ymin, xmax, ymax]

                quad = list(map(str, quad))
                corner = list(map(str, corner))
                lines += [[folder, filename, ant, *corner, *quad]]

                charind += len(ant)

    _gtmatRecognizer(csvgenerator, basedir, imagedirname, lines=lines)

    annodir = os.path.join(basedir, 'Annotations')
    with open(os.path.join(annodir, 'gt_alphanumeric.csv'), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(lines)

def get_characters(basedir, imagedirname='SynthText', skip_missing=False):

    class Symbols:
        def __init__(self):
            self.symbols = set()

        def update(self, data):
            self.symbols = self.symbols.union(data)

        def __len__(self):
            return len(self.symbols)

        def __str__(self):
            return ''.join(self.symbols)

    symbols = Symbols()

    def csvgenerator(annodir, imagedir, cbb, wBB, imname, txts, symbols, **kwargs):
        image_num = kwargs.get('image_num')
        i = kwargs.get('i')

        imgpath = os.path.join(imagedir, imname)

        img = cv2.imread(imgpath)
        h, w, _ = img.shape
        if not os.path.exists(imgpath):
            if not skip_missing:
                raise FileNotFoundError('{} was not found'.format(imgpath))
            else:
                logging.warning('Missing image: {}'.format(imgpath))
                raise _Skip()


        # convert txts to list of str
        # I don't know why txts is
        # ['Lines:\nI lost\nKevin ', 'will                ', 'line\nand            ',
        # 'and\nthe             ', '(and                ', 'the\nout             ',
        # 'you                 ', "don't\n pkg          "]
        # there is strange blank and the length of txts is different from the one of wBB
        txts = ' '.join(txts.tolist()).split()
        text_num = len(txts)

        if wBB.ndim == 2:
            # convert shape=(2, 4,) to (2, 4, 1)
            wBB = np.expand_dims(wBB, 2)

        assert text_num == wBB.shape[2], 'The length of text and wordBB must be same, but got {} and {}'.format(
            text_num, wBB.shape[2])

        # replace non-alphanumeric characters with *
        alltexts_asterisk = ''.join([re.sub(r'[^A-Za-z0-9]', '*', text) for text in txts])
        assert len(alltexts_asterisk) == cbb.shape[
            2], 'The length of characters and cbb must be same, but got {} and {}'.format(
            len(alltexts_asterisk), cbb.shape[2])
        for b in range(text_num):
            text = txts[b]

            symboltext = re.sub(r'[A-Za-z0-9]+', '', text)

            symbols.update(symboltext)

        sys.stdout.write('\r{}, and number is {}...{:0.1f}% ({}/{})'.format(symbols, len(symbols), 100 * (float(i + 1) / image_num), i + 1, image_num))
        sys.stdout.flush()

    _gtmatRecognizer(csvgenerator, basedir, imagedirname, customLog=True, symbols=symbols)

    print()
    print('symbols are {}, and number is {}'.format(symbols, len(symbols)))


def _gtmatRecognizer(generator, basedir, imagedirname='SynthText', customLog=False, **kwargs):
    """
        convert gt.mat to https://github.com/MhLiao/TextBoxes_plusplus/blob/master/data/example.xml

        <annotation>
            <folder>train_images</folder>
            <filename>img_10.jpg</filename>
            <size>
                <width>1280</width>
                <height>720</height>
                <depth>3</depth>
            </size>
            <object>
                <difficult>1</difficult>
                <content>###</content>
                <name>text</name>
                <bndbox>
                    <x1>1011</x1>
                    <y1>157</y1>
                    <x2>1079</x2>
                    <y2>160</y2>
                    <x3>1076</x3>
                    <y3>173</y3>
                    <x4>1011</x4>
                    <y4>170</y4>
                    <xmin>1011</xmin>
                    <ymin>157</ymin>
                    <xmax>1079</xmax>
                    <ymax>173</ymax>
                </bndbox>
            </object>
            .
            .
            .

        </annotation>

        :param basedir: str, directory path under \'SynthText\'(, \'licence.txt\')
        :param imagedirname: (Optional) str, image directory name including \'gt.mat\
        :return:
        """
    logging.basicConfig(level=logging.INFO)

    imagedir = os.path.join(basedir, imagedirname)
    gtpath = os.path.join(imagedir, 'gt.mat')

    annodir = os.path.join(basedir, 'Annotations')

    if not os.path.exists(gtpath):
        raise FileNotFoundError('{} was not found'.format(gtpath))

    if not os.path.exists(annodir):
        # create Annotations directory
        os.mkdir(annodir)

    """
    ref: http://www.robots.ox.ac.uk/~vgg/data/scenetext/readme.txt
    gts = dict;
        __header__: bytes
        __version__: str
        __globals__: list
        charBB: object ndarray, shape = (1, image num). 
                Character level bounding box. shape = (2=(x,y), 4=(top left,...: clockwise), BBox word num)
        wordBB: object ndarray, shape = (1, image num). 
                Word level bounding box. shape = (2=(x,y), 4=(top left,...: clockwise), BBox char num)
        imnames: object ndarray, shape = (1, image num, 1).
        txt: object ndarray, shape = (i, image num).
             Text. shape = (word num)
    """
    logging.info('Loading {} now.\nIt may take a while.'.format(gtpath))
    gts = sio.loadmat(gtpath)
    logging.info('Loaded\n'.format(gtpath))

    charBB = gts['charBB'][0]
    wordBB = gts['wordBB'][0]
    imnames = gts['imnames'][0]
    texts = gts['txt'][0]

    image_num = imnames.size

    for i, (cbb, wBB, imname, txts) in enumerate(zip(charBB, wordBB, imnames, texts)):
        imname = imname[0]

        try:
            generator(annodir, imagedir, cbb, wBB, imname, txts, i=i, image_num=image_num, **kwargs)
        except _Skip:
            pass

        if not customLog:
            sys.stdout.write('\rGenerating... {:0.1f}% ({}/{})'.format(100 * (float(i + 1) / image_num), i + 1, image_num))
        sys.stdout.flush()


    print()
    logging.info('Finished!!!')
