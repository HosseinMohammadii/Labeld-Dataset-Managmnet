import os
from os import listdir
from os.path import isfile, join
import shutil

from PIL import Image, ImageEnhance

from random import randint, random, choice

base_input_dir = "/home/hossein/yolo/merged_and_transformed/train2/"
train_dir = "train"
valid_dir = "valid"


base_output_dir = "/home/hossein/yolo/final/train"

TARGET_EACH_CLASS_SAMPLE_NUM = 400
CLASSES_NUM = 34

JUST_INFO = False


def fix_name(old_name: str, file_type) -> str:
    return old_name[:11] + '.' + file_type


def change_txt_file_classes(inputs_lines: iter) -> list:
    edited_lines = []
    for line in inputs_lines:
        phrases = line.split(' ')
        phrases[0] = str(class_map[int(phrases[0])])
        edited_lines.append(' '.join(phrases))
    return edited_lines


def get_classes(inputs_lines: iter) -> set:
    classes = set()
    for line in inputs_lines:
        phrases = line.split(' ')
        classes.add(phrases[0])
    return classes


classes_num = {}
target_class = 2
each_class_images = {}
each_class_images_just_one_class = {}

for i in range(0, CLASSES_NUM):
    each_class_images_just_one_class[str(i)] = list()
    each_class_images[str(i)] = list()

i = 1

files_list = listdir(os.path.join(base_input_dir))
for f_name in files_list:
    if not f_name.endswith('.jpg'):
        continue
    text_name = f_name.replace('.jpg', '.txt')

    with open(os.path.join(base_input_dir, text_name), 'r') as f:
        classes = get_classes(f.readlines())
        for c in classes:
            each_class_images[c].append(f_name)
            if len(classes) == 1:
                each_class_images_just_one_class[c].append(f_name)

    i += 1
    if i % 50 == 0:
        print(i, 'files processed.')


# print(each_class_images.keys())
# print(len(each_class_images.keys()))
# print(each_class_images[0])
#
# print(each_class_images[20])


def get_augmented_image(img):
    brightness_factor = 1 + choice((1, -1)) * random() * 0.25
    saturation_factor = 1 + choice((1, -1)) * random() * 0.25
    contrast_factor = 1 + choice((1, -1)) * random() * 0.2
    img1 = ImageEnhance.Brightness(img).enhance(brightness_factor)
    img2 = ImageEnhance.Color(img1).enhance(saturation_factor)
    img3 = ImageEnhance.Contrast(img2).enhance(contrast_factor)
    return img3


# all_boxes = 0
# images_with_ju
for sign_class in each_class_images_just_one_class.keys():
    # if sign_class not in range(0, 3):
    #     continue
    print('-----------------------------------------------------------------------------------------------')
    original_sign_sample_num = len(each_class_images[sign_class])
    original_imgs_index = min(original_sign_sample_num, TARGET_EACH_CLASS_SAMPLE_NUM)

    remained_num = max(0, TARGET_EACH_CLASS_SAMPLE_NUM - original_sign_sample_num)
    print('{0: <4}'.format(sign_class), '{0: <4}'.format(original_sign_sample_num),
          '{0: <4}'.format(original_imgs_index), '{0: <4}'.format(remained_num))

    if JUST_INFO:
        continue

    for n in range(0, original_imgs_index):
        img_name: str = each_class_images[sign_class][randint(0, original_sign_sample_num - 1)]
        text_name = img_name.replace('.jpg', '.txt')
        if os.path.exists(os.path.join(base_output_dir, img_name)):
            continue
        shutil.copyfile(os.path.join(base_input_dir, img_name),
                        os.path.join(base_output_dir, img_name))

        shutil.copyfile(os.path.join(base_input_dir, text_name),
                        os.path.join(base_output_dir, text_name))

    # print('sign {} with {} remained to target. {} files include just this sign'.format(sign_class, remained_num, len(
    #     each_class_images_just_one_class[sign_class])))

    # for m in range(0, remained_num):
    #     original_img_name: str = choice(list(each_class_images_just_one_class[sign_class]))
    #     original_text_name = original_img_name.replace('.jpg', '.txt')
    #
    #     augmented_img_name = original_img_name.replace('.jpg', 'augmented{}.jpg'.format(m))
    #     augmented_text_name = augmented_img_name.replace('.jpg', '.txt')
    #
    #     original_img = Image.open(os.path.join(base_input_dir, original_img_name))
    #     augmented_img = get_augmented_image(original_img)
    #
    #     augmented_img.save(os.path.join(base_output_dir, augmented_img_name), quality=95)
    #     shutil.copyfile(os.path.join(base_input_dir, original_text_name),
    #                     os.path.join(base_output_dir, augmented_text_name))

