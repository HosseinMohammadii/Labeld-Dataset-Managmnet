import os
from os import listdir
from os.path import isfile, join
import shutil
from random import choice
import random
import string

train_input_dir = "/home/hossein/yolo/finalV2-3/train-main (copy)"
INPUT_IMAGE_EXT = '.jpg'

valid_output_dir = '/home/hossein/yolo/finalV2-3/valid'

COPY = False
COPY_ONE_EXTRA_CLASS = False
COPY_TWO_EXTRA_CLASS = False

SHOW_STATS = True
SHOW_TARGET_CLASS_COUNT = True
SHOW_TARGET_CLASS_IMAGES = True

SAMPLE_FROM_EACH_CLASS = 15
CLASSES_COUNT = 34


files = os.listdir(train_input_dir)
i = 0

while i < SAMPLE_FROM_EACH_CLASS * CLASSES_COUNT :
    f = choice(files)
    if not f.endswith('.txt'):
        continue
    text_name = f
    img_name = f.replace('.txt', INPUT_IMAGE_EXT)

    shutil.move(os.path.join(train_input_dir, text_name),
                os.path.join(valid_output_dir, text_name))
    shutil.move(os.path.join(train_input_dir, img_name),
                os.path.join(valid_output_dir, img_name))

    files.remove(text_name)
    files.remove(img_name)

    i += 1
