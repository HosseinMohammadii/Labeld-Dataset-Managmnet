import os
from os import listdir
from os.path import isfile, join
import shutil

import os
from os import listdir
from os.path import isfile, join
import shutil

from PIL import Image, ImageEnhance

from random import randint, random, choice


base_input_dir = "/home/hossein/yolo/finalV2-3"
train_dir = "train"
valid_dir = "valid"

base_output_dir = "/home/hossein/yolo/final4"


def get_classes(inputs_lines: iter) -> set:
    classess = set()
    for line in inputs_lines:
        phrases = line.split(' ')
        classess.add(phrases[0])
    return classess




classes_num = {}
target_class = 2
each_class_images = {}
each_class_images_just_one_class = {}

for i in range(0, 35):
    each_class_images_just_one_class[str(i)] = set()
    each_class_images[str(i)] = set()

print(os.path.join(base_input_dir), '\nto\n', os.path.join(base_output_dir))

i = 1
for subdir in (train_dir,):
    files_list = listdir(os.path.join(base_input_dir, subdir))
    for f_name in files_list:
        if not f_name.endswith('.jpg'):
            continue
        text_name = f_name.replace('.jpg', '.txt')

        with open(os.path.join(base_input_dir, subdir, text_name), 'r') as f:
            classes = get_classes(f.readlines())
            for c in classes:
                each_class_images[c] = each_class_images[c].union({os.path.join(subdir, f_name)})
                if len(classes) == 1:
                    each_class_images_just_one_class[c].add(os.path.join(subdir, f_name))

        i += 1
        if i % 50 == 0:
            print(i, 'files processed.')

for sign_class in each_class_images_just_one_class.keys():
    print(sign_class)
    # if sign_class not in range(0, 3):
    #     continue
    # print('-----------------------------------------------------------------------------------------------')
    # original_sign_sample_num = len(each_class_images[sign_class])
    # original_imgs_index = min(original_sign_sample_num, TARGET_EACH_CLASS_SAMPLE_NUM)
    #
    # remained_num = max(0, TARGET_EACH_CLASS_SAMPLE_NUM - original_sign_sample_num)
    # print('{0: <4}'.format(sign_class), '{0: <4}'.format(original_sign_sample_num),
    #       '{0: <4}'.format(original_imgs_index), '{0: <4}'.format(remained_num))

    # n = 0
    # nn = 0
    # while n < 7:
    #     if nn < 20:
    #
    #         img_name: str = choice(list(each_class_images_just_one_class[sign_class]))
    #     else:
    #         img_name: str = choice(list(each_class_images[sign_class]))
    #     nn += 1
    #     text_name = img_name.replace('.jpg', '.txt')
    #     if not os.path.exists(os.path.join(base_input_dir, img_name)):
    #         continue
    #     shutil.move(os.path.join(base_input_dir, img_name),
    #                 os.path.join(base_output_dir, valid_dir, img_name.replace('train/', '')))
    #     shutil.move(os.path.join(base_input_dir, text_name),
    #                 os.path.join(base_output_dir, valid_dir, text_name.replace('train/', '')))
    #     n += 1
