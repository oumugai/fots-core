import os

from .._utils import DATA_ROOT

import re
import pandas as pd

df = pd.read_csv("./joyo.txt", header=None, skiprows=1, delimiter='\t')

hiragana = \
['あ','い','う','え','お','か','き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て',
'と','な','に','ぬ','ね','の','は','ひ','ふ','へ','ほ','ま','み','む','め','も','ら','り','る',
'れ','ろ','が','ぎ','ぐ','げ','ご','ざ','じ','ず','ぜ','ぞ','だ','ぢ','づ','で','ど','ば','び',
'ぶ','べ','ぼ','ぱ','ぴ','ぷ','ぺ','ぽ','や','ゆ','よ','わ','を','ん',"ぁ", "ぃ", "ぅ", "ぇ", "ぉ", "っ", "ゃ", "ゅ", "ょ", "ゎ"]

katakana = \
['ア','イ','ウ','エ','オ','カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ',
'ト','ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ','ヘ','ホ','マ','ミ','ム','メ','モ','ラ','リ','ル',
'レ','ロ','ガ','ギ','グ','ゲ','ゴ','ザ','ジ','ズ','ゼ','ゾ','ダ','ヂ','ヅ','デ','ド','バ','ビ',
'ブ','ベ','ボ','パ','ピ','プ','ペ','ポ','ヤ','ユ','ヨ','ワ','ヲ','ン','ー',"ァ", "ィ", "ゥ", "ェ", "ォ", "ッ", "ャ", "ュ", "ョ", "ヮ"]

alphabet_upper = \
['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',
'W','X','Y','Z']

alphabet_lower = \
['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v',
'w','x','y','z']

numetric = ['0','1','2','3','4','5','6','7','8','9']

alphabet_num = alphabet_upper + alphabet_lower + numetric

kigou = \
['(',')','[',']','「','」','『','』','<','>','¥','/','÷','*','+','×','?','=','〜','|',':',
';','。','、','.',',', "&", "【", "】", "\n", "・", '”', "'", "-", "■"]

jyouyou_kanji = ''.join(df.iloc[:, 0])

nihongo = hiragana+katakana+alphabet_num+kigou+jyouyou_kanji

SynthText_class_labels = ['text']
SynthText_class_nums = len(SynthText_class_labels)

#SynthText_char_labels_with_upper = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
SynthText_char_labels_with_upper = nihongo
SynthText_char_nums_with_upper = len(SynthText_char_labels_with_upper)

SynthText_char_labels_with_upper_blank = [' '] + SynthText_char_labels_with_upper
SynthText_char_nums_with_upper_blank = len(SynthText_char_labels_with_upper_blank)

#SynthText_char_labels_without_upper = list('0123456789abcdefghijklmnopqrstuvwxyz!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
SynthText_char_labels_without_upper = nihongo
SynthText_char_nums_without_upper = len(SynthText_char_labels_without_upper)

SynthText_char_labels_without_upper_blank = [' '] + SynthText_char_labels_without_upper
SynthText_char_nums_without_upper_blank = len(SynthText_char_labels_without_upper_blank)

SynthText_ROOT = os.path.join(DATA_ROOT, 'text', 'SynthText')