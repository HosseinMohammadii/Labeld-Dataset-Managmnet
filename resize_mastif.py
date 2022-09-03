from PIL import Image
from PIL import ImageOps

import os
from os import listdir
from os.path import isfile, join

base_input_dir = "/home/hossein/yolo/mastif_uniq_aug/train"
train_dir = "train"
valid_dir = "valid"

base_output_dir = "/home/hossein/yolo/mastif_uniq_aug_resized/train/2"

target_width = 864
target_height = 864


def get_new_y_centers(boxes, img_sizes, scale_factor) -> list:
    new_boxes = []
    for box in boxes:
        details = box.split(' ')
        old_y_center = float(details[2]) * img_sizes[1] * scale_factor
        t2 = (target_height - img_sizes[1] * scale_factor) / 2
        new_y_center = (old_y_center + t2) / target_height
        details[2] = str(new_y_center)
        new_boxes.append(' '.join(details))
    return new_boxes


def get_resized_image(img):
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
            img_name = f_name.replace('.txt', '.jpg')
            old_img = Image.open(os.path.join(base_input_dir, img_name))
            old_sizes = old_img.size
            new_img, scale_factor = get_resized_image(old_img)
            new_lines = get_new_y_centers(text_f.readlines(), old_sizes, scale_factor)

            with open(os.path.join(base_output_dir, f_name), 'w') as new_text_f:
                new_text_f.writelines(new_lines)

            new_img.save(os.path.join(base_output_dir, img_name), quality=97)

    i += 1
    if i % 50 == 0:
        print(i, 'files processed.')

# print(collect_img_sizes)
