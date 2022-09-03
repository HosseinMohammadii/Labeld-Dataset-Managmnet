import os
from os import listdir
from os.path import isfile, join
import shutil

# from roboflow alphabet sorted to gtsdb sequence


# l = sorted(class_map.items(), key=lambda x: x[1])
# print(l)

base_input_dir = "../full_gtsdb"
train_dir = "train"
valid_dir = "valid"


# base_output_dir = "/home/hossein/yolo/gtsdb_strain/"

classes_num = {}
target_class = 6
target_class_images = []
image_width = 1088
crop_width = 1088


def fix_name(old_name: str, file_type) -> str:
    return old_name[:11] + '.' + file_type


def change_txt_file_classes(inputs_lines: iter) -> list:
    edited_lines = []
    for line in inputs_lines:
        phrases = line.split(' ')
        phrases[0] = str(class_map[int(phrases[0])])
        edited_lines.append(' '.join(phrases))
    return edited_lines


def get_least_last_xcordinate(inputs_lines: iter) -> list:
    widths = []
    for line in inputs_lines:
        phrases = line.split(' ')
        t1 = float(phrases[2]) * image_width - float(phrases[4]) * image_width
        t2 = float(phrases[2]) * image_width + float(phrases[4]) * image_width
        widths.append((t1, t2))
    return widths


i = 0
before_crop = 0
after_crop = 0
before_crops = []
after_crops = []

before_crop_index = (image_width - crop_width) / 2
after_crop_index = (image_width - crop_width) / 2 + crop_width
for subdir in (train_dir, valid_dir):
    files_list = listdir(os.path.join(base_input_dir, subdir))
    for f_name in files_list:
        if f_name.endswith('txt'):
            with open(os.path.join(base_input_dir, subdir, f_name), 'r') as f:
                for xcord in get_least_last_xcordinate(f.readlines()):
                    i += 1
                    if xcord[0] < before_crop_index:
                        print(xcord[0], xcord[1])
                        before_crop += 1
                        before_crops.append(os.path.join(base_input_dir, subdir, f_name))
                    elif xcord[1] > after_crop_index:
                        after_crop += 1
                        after_crops.append(os.path.join(base_input_dir, subdir, f_name))

print('before_crop_index', before_crop_index)
print('after_crop_index', after_crop_index)
print('all_objects', i)
print('before_crop', before_crop)
print("after_crop", after_crop)
print('clean_objects', i - before_crop - after_crop)

print('before_crops:\n', before_crops)
print('after_crops:\n', after_crops)






























