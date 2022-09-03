from PIL import Image
from PIL import ImageOps
import imageio

import os
from os import listdir
from os.path import isfile, join

from math import fabs

base_input_dir = "/home/hossein/yolo/gtsdb_aug/train"
train_dir = "train"
valid_dir = "valid"

base_output_dir = "/home/hossein/yolo/gtsdb_aug_resized/train2"

target_width = 864
target_height = 864


def get_new_y_centers(boxes, img_sizes, scale_factorr) -> list:
    # print(scale_factorr)
    new_boxes = []
    for box in boxes:
        details = box.split(' ')
        old_y_center = float(details[2]) * img_sizes[1] * scale_factorr
        t2 = (target_height - img_sizes[1] * scale_factorr) / 2
        new_y_center = (old_y_center + t2) / target_height
        details[2] = str(new_y_center)
        new_boxes.append(' '.join(details))
    return new_boxes


def calculate_scale_factor(boxess, w, h):
    return 1
    if len(boxess) == 0:
        return 1
    min_scale_factor = 100
    for boxx in boxess:
        detailss = boxx.split(' ')
        right = fabs(float(detailss[1]) + float(detailss[3]) - 0.5) * 2
        left = fabs(float(detailss[1]) - float(detailss[3]) - 0.5) * 2
        top = fabs(float(detailss[2]) - float(detailss[4]) - 0.5) * 2
        bottom = fabs(float(detailss[2]) + float(detailss[4]) - 0.5) * 2

        sf1 = 1 / right
        sf2 = 1 / left
        sf3 = 1 / top
        sf4 = 1 / bottom
        min_scale_factor = min((min_scale_factor, sf1, sf2, sf3, sf4))

    return min_scale_factor - 0.01


# def get_resized_image(img, minimum_scale_factor):
#     old_sizes_o = img.size
#     scale_factor = minimum_scale_factor
#     img = ImageOps.scale(img, scale_factor)
#     img_sizes = img.size
#
#     new_sizes = old_sizes_o
#     new_im = Image.new("RGB", new_sizes)  ## luckily, this is already black!
#
#     new_im.paste(img, ((new_sizes[0] - img_sizes[0]) // 2,
#                        (new_sizes[1] - img_sizes[1]) // 2))
#     return new_im, scale_factor


# def get_resized_image(img, minimum_scale_factor):
#     t_img = ImageOps.scale(img, minimum_scale_factor)
#     t_img_sizes = t_img.size
#
#     scale_factor = target_height / max(t_img_sizes)
#     # print(scale_factor)
#     # print("scale_factor", scale_factor)
#     img = ImageOps.scale(t_img, scale_factor)
#     img_sizes = img.size
#
#     new_sizes = (target_width, target_height)
#     new_im = Image.new("RGB", new_sizes)  ## luckily, this is already black!
#
#     new_im.paste(img, ((new_sizes[0] - img_sizes[0]) // 2,
#                        (new_sizes[1] - img_sizes[1]) // 2))
#     return new_im, scale_factor


def get_resized_image(img, minimum_scale_factor):
    img_sizes = img.size
    scale_factor = target_height / max(img_sizes)
    img = ImageOps.scale(img, scale_factor)
    img_sizes = img.size

    new_sizes = (target_width, target_height)
    new_im = Image.new("RGB", new_sizes)  ## luckily, this is already black!

    new_im.paste(img, ((new_sizes[0] - img_sizes[0]) // 2,
                       (new_sizes[1] - img_sizes[1]) // 2))
    return new_im, scale_factor


collect_img_sizes = {}

i = 0
files_list = listdir(base_input_dir)
for f_name in files_list:
    if f_name.endswith('txt'):
        with open(os.path.join(base_input_dir, f_name), 'r') as text_f:
            # print('--------------------------------------')
            # print()
            img_name = f_name.replace('.txt', '.jpg')
            old_img = Image.open(os.path.join(base_input_dir, img_name))
            old_sizes = old_img.size
            f_boxes = text_f.readlines()
            new_img, scale_factor_inja = get_resized_image(old_img, calculate_scale_factor(f_boxes, *old_sizes))
            new_lines = get_new_y_centers(f_boxes, old_sizes, scale_factor_inja)

            with open(os.path.join(base_output_dir, f_name), 'w') as new_text_f:
                new_text_f.writelines(new_lines)

            imageio.imsave(os.path.join(base_output_dir, img_name), new_img, quality=96)
            # new_img.save(os.path.join(base_output_dir, img_name), quality=97)

    i += 1
    if i % 50 == 0:
        print(i, 'files processed.')

# print(collect_img_sizes)
