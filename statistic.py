import os
from os import listdir
from os.path import isfile, join
import shutil
from random import choice
import random
import string

# from roboflow alphabet sorted to gtsdb sequence


# INPUT_IMAGE_EXT = '.jpg'

# base_input_dir = "/home/hossein/yolo/gtsdb/train"
# INPUT_IMAGE_EXT = '.png'
#
base_input_dir = "/home/hossein/yolo/finalV2-3/valid"
INPUT_IMAGE_EXT = '.jpg'

# base_output_dir = '/home/hossein/yolo/finalV2_2/32'

target_class = 11
TARGET_CLASS_COPY_SAMPLE_NUM = 100

COPY = False
COPY_ONE_EXTRA_CLASS = False
COPY_TWO_EXTRA_CLASS = False

SHOW_STATS = True
SHOW_TARGET_CLASS_COUNT = True
SHOW_TARGET_CLASS_IMAGES = True


train_dir = "train"
valid_dir = "valid"
print(base_input_dir)
#base_output_dir = "/home/hossein/yolo/gtsdb_strain/"

img_files_count = 0
txt_files_count = 0

def fix_name(old_name: str, file_type) -> str:
    return old_name[:11] + '.' + file_type


def change_txt_file_classes(inputs_lines: iter) -> list:
    edited_lines = []
    for line in inputs_lines:
        phrases = line.split(' ')
        phrases[0] = str(class_map[int(phrases[0])])
        edited_lines.append(' '.join(phrases))
    return edited_lines


def get_classes(inputs_lines: iter) -> list:
    classes = []
    for line in inputs_lines:
        phrases = line.split(' ')
        classes.append(int(phrases[0]))
    return classes
    
    
classes_num = {}
target_class_images = []
target_class_images_just_target = []
target_class_images_just_target_plus_one_extra = []
target_class_images_just_target_plus_two_extra = []

i = 1
# for subdir in (valid_dir,):
files_list = listdir(os.path.join(base_input_dir))
for f_name in files_list:
    if f_name.endswith(INPUT_IMAGE_EXT):
        img_files_count += 1
        f_name = f_name.replace(INPUT_IMAGE_EXT, '.txt')
        with open(os.path.join(base_input_dir, f_name), 'r') as f:
            classes = get_classes(f.readlines())
            classes = list(set(classes))
            for c in classes:
                classes_num[c] = classes_num.get(c, 0) + 1
                i += 1
                if c == target_class:
                    target_class_images.append(f_name)
                    if len(classes) == 1:
                        target_class_images_just_target.append(f_name)
                    if len(classes) == 2:
                        target_class_images_just_target_plus_one_extra.append(f_name)
                    if len(classes) == 3:
                        target_class_images_just_target_plus_two_extra.append(f_name)
    elif f_name.endswith('.txt'):
        txt_files_count += 1

     # i += 1
     # if i % 50 == 0:
     #     print(i, 'files processed.')


if SHOW_STATS:
    print('imgs: {}  txts: {}  all: {}'.format(img_files_count, txt_files_count, (txt_files_count + img_files_count)))
    l = sorted(classes_num.items(), key=lambda x: x[0])
    max_num = max(classes_num.values())

    for c in l:
       s = ''
       ss = int(c[1] / max_num * 40)
       for i in range(0, ss):
           s += '#'

       # '{0: <3}'.format(str(c[0])),
       print('{0: <3}'.format(str(c[0])), '{0: <3}'.format(str(c[1])), ' : ', s)


# print and gather target


# if COPY:
#     target_class_images_just_target.sort()
#     print('just_target', len(target_class_images_just_target))
#     for f in target_class_images_just_target:
#         text_name = f
#         img_name = f.replace('.txt', INPUT_IMAGE_EXT)
#         print('    "'+img_name+'": ,')
#         shutil.copyfile(os.path.join(base_input_dir, text_name),
#                         os.path.join(base_output_dir, text_name))
#         shutil.copyfile(os.path.join(base_input_dir, img_name),
#                         os.path.join(base_output_dir, img_name))
#
#
# if COPY and COPY_ONE_EXTRA_CLASS:
#     target_class_images_just_target_plus_one_extra.sort()
#     print('just_target_plus_ONE_extra', len(target_class_images_just_target_plus_one_extra))
#     for f in target_class_images_just_target_plus_one_extra:
#         text_name = f
#         img_name = f.replace('.txt', INPUT_IMAGE_EXT)
#         print('    "'+img_name+'": ,')
#         shutil.copyfile(os.path.join(base_input_dir, text_name),
#                         os.path.join(base_output_dir, text_name))
#         shutil.copyfile(os.path.join(base_input_dir, img_name),
#                         os.path.join(base_output_dir, img_name))
#
#
# if COPY and COPY_TWO_EXTRA_CLASS:
#     target_class_images_just_target_plus_two_extra.sort()
#     print('just_target_plus_TWO_extra', len(target_class_images_just_target_plus_two_extra))
#     for f in target_class_images_just_target_plus_two_extra:
#         text_name = f
#         img_name = f.replace('.txt', INPUT_IMAGE_EXT)
#         print('    "'+img_name+'": ,')
#         shutil.copyfile(os.path.join(base_input_dir, text_name),
#                         os.path.join(base_output_dir, text_name))
#         shutil.copyfile(os.path.join(base_input_dir, img_name),
#                         os.path.join(base_output_dir, img_name))


if SHOW_TARGET_CLASS_COUNT:
    print('class {}: {} objects'.format(target_class, len(target_class_images)))
if SHOW_TARGET_CLASS_IMAGES:
    print('class {} files: '.format(target_class))
    target_class_images.sort()
    for f in target_class_images:
        print('    "'+f.replace('.txt', '.jpg')+'": 0,')


# -------------------------------------------------------------------------

def id_generator(size=3, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# if COPY:
#     target_class_images_just_target.sort()
#     print(target_class, len(target_class_images_just_target), TARGET_CLASS_COPY_SAMPLE_NUM)
#
#     iterate_index = min(len(target_class_images_just_target), TARGET_CLASS_COPY_SAMPLE_NUM, )
#
#     TARGET_CLASS_COPY_SAMPLE_NUM = TARGET_CLASS_COPY_SAMPLE_NUM - len(target_class_images_just_target)
#     if TARGET_CLASS_COPY_SAMPLE_NUM < 0:
#         TARGET_CLASS_COPY_SAMPLE_NUM = 0
#
#     for i in range(0, iterate_index):
#         f = choice(target_class_images_just_target)
#         text_name = f
#         img_name = f.replace('.txt', INPUT_IMAGE_EXT)
#
#         new_text_name = text_name.replace('.txt', '') + id_generator() + '.txt'
#         new_img_name = new_text_name.replace('.txt', '.jpg')
#
#         shutil.copyfile(os.path.join(base_input_dir, text_name),
#                         os.path.join(base_output_dir, new_text_name))
#         shutil.copyfile(os.path.join(base_input_dir, img_name),
#                         os.path.join(base_output_dir, new_img_name))
#
#         target_class_images_just_target.remove(f)
#
# if COPY and COPY_ONE_EXTRA_CLASS:
#     target_class_images_just_target_plus_one_extra.sort()
#     print(len(target_class_images_just_target_plus_one_extra))
#     iterate_index = min(len(target_class_images_just_target_plus_one_extra), TARGET_CLASS_COPY_SAMPLE_NUM, )
#
#     TARGET_CLASS_COPY_SAMPLE_NUM = TARGET_CLASS_COPY_SAMPLE_NUM - len(target_class_images_just_target_plus_one_extra)
#     if TARGET_CLASS_COPY_SAMPLE_NUM < 0:
#         TARGET_CLASS_COPY_SAMPLE_NUM = 0
#
#     for i in range(0, iterate_index):
#         f = choice(target_class_images_just_target_plus_one_extra)
#         text_name = f
#         img_name = f.replace('.txt', INPUT_IMAGE_EXT)
#
#         new_text_name = text_name.replace('.txt', '') + id_generator() + '.txt'
#         new_img_name = new_text_name.replace('.txt', '.jpg')
#
#         shutil.copyfile(os.path.join(base_input_dir, text_name),
#                         os.path.join(base_output_dir, new_text_name))
#         shutil.copyfile(os.path.join(base_input_dir, img_name),
#                         os.path.join(base_output_dir, new_img_name))
#
#         target_class_images_just_target_plus_one_extra.remove(f)
#
# if COPY and COPY_TWO_EXTRA_CLASS:
#     target_class_images_just_target_plus_two_extra.sort()
#     print(len(target_class_images_just_target_plus_two_extra))
#     iterate_index = min(len(target_class_images_just_target_plus_two_extra), TARGET_CLASS_COPY_SAMPLE_NUM, )
#
#     TARGET_CLASS_COPY_SAMPLE_NUM = TARGET_CLASS_COPY_SAMPLE_NUM - len(target_class_images_just_target_plus_two_extra)
#     if TARGET_CLASS_COPY_SAMPLE_NUM < 0:
#         TARGET_CLASS_COPY_SAMPLE_NUM = 0
#
#     for i in range(0, iterate_index):
#         f = choice(target_class_images_just_target_plus_two_extra)
#         text_name = f
#         img_name = f.replace('.txt', INPUT_IMAGE_EXT)
#
#         new_text_name = text_name.replace('.txt', '') + id_generator() + '.txt'
#         new_img_name = new_text_name.replace('.txt', '.jpg')
#
#         shutil.copyfile(os.path.join(base_input_dir, text_name),
#                         os.path.join(base_output_dir, new_text_name))
#         shutil.copyfile(os.path.join(base_input_dir, img_name),
#                         os.path.join(base_output_dir, new_img_name))
#
#         target_class_images_just_target_plus_two_extra.remove(f)
#
#
# if COPY:
#     print('{} files remained and not in folder'.format(TARGET_CLASS_COPY_SAMPLE_NUM))
























