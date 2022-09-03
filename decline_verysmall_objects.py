from PIL import Image
from PIL import ImageOps

import os
from os import listdir
from os.path import isfile, join
import shutil

base_input_dir = "/home/hossein/yolo/mastif_uniq_aug_resized/train3"
train_dir = "train"
valid_dir = "valid"

base_output_dir = "/home/hossein/yolo/mastif_uniq_aug_resized_filtered/train"
include_negatives = True


print(base_input_dir, '\nto\n', base_output_dir)


"""
 the least area of acceptable objects
 mastif 800 x 800 : 0.0014
 gtsdb 800 * 800 : 0.0007 because of better quality
 
  the least area of acceptable objects
 mastif 864 x 864 : 0.0025
 gtsdb 864 * 864 : 0.0046 because of better quality
"""

MIN_ACCEPTABLE_AREA = 0.0046

def get_filtered_boxes(boxes) -> list:
    new_boxes = []
    for box in boxes:
        details = box.split(' ')
        if float(details[3]) * float(details[4]) > MIN_ACCEPTABLE_AREA:
            new_boxes.append(' '.join(details))
    return new_boxes


collect_img_sizes = {}

i = 0
declined_cases = []
files_list = listdir(base_input_dir)
for f_name in files_list:
    if f_name.endswith('txt'):
        with open(os.path.join(base_input_dir, f_name), 'r') as text_f:
            img_name = f_name.replace('.txt', '.jpg')
            old_boxes = text_f.readlines()
            new_boxes = get_filtered_boxes(old_boxes)
            if len(new_boxes) < 1:
                declined_cases.append(img_name)
                if len(old_boxes) > 0:
                    continue
            shutil.copyfile(os.path.join(base_input_dir, img_name),
                            os.path.join(base_output_dir, img_name))
            with open(os.path.join(base_output_dir, f_name), 'w') as new_text_f:
                new_text_f.writelines(new_boxes)
    i += 1
    if i % 50 == 0:
        print(i, 'files processed.')

print(len(declined_cases))
declined_cases.sort()
for case in declined_cases:
    print(case)
