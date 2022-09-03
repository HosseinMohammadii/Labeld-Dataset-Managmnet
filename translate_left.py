import random
import string
from math import fabs

import imageio
import imgaug as ia
from imgaug import augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from imgaug.augmentables.batches import Batch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

base_input_dir = '/home/hossein/yolo/final3/raw_c28'
# base_input_dir0 = '/home/hossein/yolo/gtsdb/train'
# base_input_dir1 = '/home/hossein/yolo/mastif_uniq/train'

base_output_dir = '/home/hossein/yolo/final3/raw_c28'
output_width = 864
output_height = 864

# gtsdb 1360 x 800 min useful object area: 0.0010
# mastif 720 * 576 min useful object area: 0.0024

# if just crop, then decrease this value
MIN_ACCEPTABLE_AREA = 0.0001
GTSDB = True
MASTIF = True

FINAL_CLASS_IMAGES_NUM = 260

CURRENT_CLASS_STAS = {
    28: (100, 5, 1),
}

MOST_REPETANCE_CLASS_THRESH = 300

# This section does the translation job too

old_class_path = '/home/hossein/yolo/merged_and_transformed/obj.labels'
new_class_path = '/home/hossein/yolo/final2/obj.labels'
# new_class_path = old_class_path

"""
class_map = {old_class_line: new_class_line}raw_c30_aug
"""
class_map = {}


def id_generator(size=3, chars=string.ascii_uppercase + string.digits):
    # return 'flip'
    return 'translated_left'
    return ''.join(random.choice(chars) for _ in range(size))


with open(new_class_path, 'r') as new_class_f:
    new_classes = new_class_f.readlines()
    with open(old_class_path, 'r') as old_class_f:
        old_classes = old_class_f.readlines()

        for i in range(0, len(old_classes)):
            for j in range(0, len(new_classes)):
                if old_classes[i] == new_classes[j]:
                    class_map[i] = j
                    break


def translate_class(label: str) -> str:
    try:
        return str(class_map[int(label)])
    except Exception:
        return ''


def get_translated_yolo_boxes(yolo_boxes: iter) -> list:
    translated_boxes = []
    for box in yolo_boxes:
        phrases = box.split(' ')
        translated_class = translate_class(phrases[0])
        if translated_class != '':
            phrases[0] = translated_class
            translated_boxes.append(' '.join(phrases))
    return translated_boxes


def get_classes_of_yolo_boxes(yolo_boxes: iter) -> set:
    classes = set()
    for box in yolo_boxes:
        phrases = box.split(' ')
        classes.add(int(phrases[0]))
    return classes


def get_filtered_yolo_boxes(boxes) -> (list, float):
    new_boxes = []
    min_area = 1
    for box in boxes:
        details = box.split(' ')
        area = float(details[3]) * float(details[4])
        if float(details[3]) * float(details[4]) > MIN_ACCEPTABLE_AREA:
            new_boxes.append(' '.join(details))
            min_area = min(min_area, area)

    if len(new_boxes) == 0:
        min_area = 0.0005

    return new_boxes, min_area


def get_converted_to_aug_boxes(boxes, image):
    new_boxes = []
    img_sizes = image.shape
    for box in boxes:
        details = box.split(' ')
        right = float(details[1]) + float(details[3]) / 2
        left = float(details[1]) - float(details[3]) / 2
        top = float(details[2]) - float(details[4]) / 2
        bottom = float(details[2]) + float(details[4]) / 2
        new_boxes.append(BoundingBox(label=details[0], x1=left * img_sizes[1], x2=right * img_sizes[1],
                                     y1=top * img_sizes[0], y2=bottom * img_sizes[0]), )
    # new_boxes.append(BoundingBox(0, 0, 0, 0))
    return BoundingBoxesOnImage(new_boxes, shape=image.shape)


def get_converted_to_yolo_boxes(boxes, shape):
    new_boxes = []
    for box in boxes:
        details = []
        details.append(str(box.label))
        details.append(str((box.x1 + box.x2) / (2 * shape[1])))
        details.append(str((box.y1 + box.y2) / (2 * shape[0])))
        details.append(str((box.x2 - box.x1) / shape[1]))
        details.append(str((box.y2 - box.y1) / shape[0]))
        new_box = ' '.join(details) + '\n'
        # print(new_box, end='')
        new_boxes.append(new_box)
    return new_boxes


def get_filtered_aug_boxes(boxes, shape) -> BoundingBoxesOnImage:
    # return BoundingBoxesOnImage(boxes, shape=shape)
    x_check_attrs = ('x1', 'x2')
    y_check_attrs = ('y1', 'y2')
    new_boxes = []
    for box in boxes:
        valid = True

        wid = (box.x2 - box.x1) / 2.8
        hei = (box.y2 - box.y1) / 2.8
        for attr in x_check_attrs:
            val = getattr(box, attr)
            # print(val, wid)
            if val < 0 - wid or val > shape[1] + wid:
                valid = False

        for attr in y_check_attrs:
            val = getattr(box, attr)
            # print(val, hei)
            if val < 0 - hei or val > shape[0] + hei:
                valid = False

        if not valid:
            continue

        new_boxes.append(box)

    return BoundingBoxesOnImage(new_boxes, shape=shape)


def get_classes_of_aug_boxes(aug_boxes: iter) -> set:
    classes = set()
    for box in aug_boxes:
        classes.add(int(box.label))
    return classes


def save(image, image_name: str, boxes, output_path, img_ext='.jpg', old_img_ext='.png', aug_postfix=None) -> bool:
    pure_image_name = image_name.replace(old_img_ext, '')
    if aug_postfix is not None:
        pure_image_name += '-aug-' + id_generator() + str(aug_postfix)
    image_name = pure_image_name + img_ext
    text_name = image_name.replace(img_ext, '.txt')

    yolo_boxes = get_converted_to_yolo_boxes(boxes, image.shape)
    if len(yolo_boxes) == 0:
        return False

    imageio.imsave(os.path.join(output_path, image_name), image, quality=95)
    text_f = open(os.path.join(output_path, text_name), 'w')
    text_f.writelines(yolo_boxes)
    text_f.close()
    return True


def get_proper_pipeline(area):
    # return just_crop_pipeline
    # if GTSDB:
    #     return iaa.Sequential([iaa.Fliplr(p=1.0)])
    #
    # if MASTIF:
    #     return iaa.Sequential([iaa.Fliplr(p=1.0)])

    if GTSDB:
        return iaa.Sequential([iaa.TranslateX(percent=(-0.5, -0.3))])

    if MASTIF:
        return iaa.Sequential([iaa.TranslateX(percent=(-0.5, -0.3))])


# fig, axes = plt.subplots(5, 5, figsize=(16, 16))
# axes = axes.flatten()


def augment_and_save(output_target_class, required_augmented_images_of_target_class_num, extra_allowed_class_num,
                     base_input_dir, input_img_ext='.jpg', output_image_ext='.jpg', every_image_repetance=5):
    accepted_images_for_target_class = 0
    process_image_num = 0
    input_files_list = os.listdir(base_input_dir)
    for img_name in input_files_list:
        if accepted_images_for_target_class > required_augmented_images_of_target_class_num:
            break

        if 'gtsdb' in img_name:
            # print('gtsdb')
            MIN_ACCEPTABLE_AREA = 0.0010
            GTSDB = True
            MASTIF = False
            input_img_ext = '.png'

        elif 'mastif' in img_name:
            # print('mastif')
            MIN_ACCEPTABLE_AREA = 0.0027
            GTSDB = False
            MASTIF = True
            input_img_ext = '.jpg'

        if not img_name.endswith(input_img_ext):
            continue

        process_image_num += 1
        image = imageio.imread(os.path.join(base_input_dir, img_name))

        text_name = img_name.replace(input_img_ext, '.txt')
        text = open(os.path.join(base_input_dir, text_name), 'r')

        translated_yolo_boxes = get_translated_yolo_boxes(text.readlines())
        image_contained_classes = get_classes_of_yolo_boxes(translated_yolo_boxes)
        image_contained_classes = list(image_contained_classes)
        is_proper_image = len(image_contained_classes) <= 1 + extra_allowed_class_num and \
                          (output_target_class in image_contained_classes)

        # print(img_name, '\n',
        #       is_proper_image, '\n',
        #       len(image_contained_classes), extra_allowed_class_num, '\n',
        #       output_target_class, image_contained_classes)

        for cla in image_contained_classes:
            try:
                if CURRENT_CLASS_STAS[cla][0] > MOST_REPETANCE_CLASS_THRESH:
                    is_proper_image = False
            except:
                pass

        # print(is_proper_image)
        if not is_proper_image:
            continue

        yolo_filtered_boxes, min_area = get_filtered_yolo_boxes(translated_yolo_boxes)
        bbs = get_converted_to_aug_boxes(yolo_filtered_boxes, image)
        # ia.imshow(bbs.draw_on_image(image, size=2))
        ppln = get_proper_pipeline(min_area)
        text.close()

        print(process_image_num, '---', img_name)

        original_augmented_images_names = open(
            os.path.join(base_output_dir, '..', 'original_augmented_images_names.txt'),
            'a')

        for j in range(0, every_image_repetance):
            ppln.random_order = True
            image_aug, bbs_aug = ppln(image=image, bounding_boxes=bbs)
            # print('BBS AUG')
            # print(bbs_aug)
            bbs_aug = get_filtered_aug_boxes(bbs_aug.bounding_boxes, bbs_aug.shape)
            bbs_aug = bbs_aug.clip_out_of_image()

            aug_image_contained_classes = get_classes_of_aug_boxes(bbs_aug.bounding_boxes)
            is_proper_aug_image = output_target_class in aug_image_contained_classes

            # print("is_proper_aug_image", is_proper_aug_image)
            if not is_proper_aug_image:
                continue

            is_saved = save(image_aug, img_name, bbs_aug.bounding_boxes, base_output_dir,
                            output_image_ext, input_img_ext, j)
            if is_saved:
                accepted_images_for_target_class += 1
            if accepted_images_for_target_class > required_augmented_images_of_target_class_num:
                break

        original_augmented_images_names.write(img_name + '\n')
        original_augmented_images_names.close()

    return accepted_images_for_target_class


for cl in CURRENT_CLASS_STAS.keys():
    OUTPUT_TARGET_CLASS = cl
    EXTRA_ALLOWED_CLASS_NUM = 5
    REQUIRED_AUGMENTED_IMAGES_OF_TARGET_CLASS_NUM = FINAL_CLASS_IMAGES_NUM - CURRENT_CLASS_STAS[cl][0]
    RAIOTCN = REQUIRED_AUGMENTED_IMAGES_OF_TARGET_CLASS_NUM
    RAIOTCN = 280

    if RAIOTCN <= 0:
        print(cl, RAIOTCN, EXTRA_ALLOWED_CLASS_NUM, '        SKIPPED')
        continue

    # RAIOTCN = int(min(RAIOTCN, 180))
    # RAIOTCN = int(RAIOTCN / 2)

    print(cl, RAIOTCN, EXTRA_ALLOWED_CLASS_NUM)

    # MIN_ACCEPTABLE_AREA = 0.0010
    # GTSDB = True
    # MASTIF = False
    added_images_num = augment_and_save(cl, RAIOTCN, EXTRA_ALLOWED_CLASS_NUM, base_input_dir, '.png',
                                        '.jpg', CURRENT_CLASS_STAS[cl][2])

    print('added_images_num', added_images_num)

    # MIN_ACCEPTABLE_AREA = 0.0027
    # GTSDB = False
    # MASTIF = True
    # augment_and_save(cl, RAIOTCN - added_images_num, EXTRA_ALLOWED_CLASS_NUM, base_input_dir1, '.jpg', '.jpg')
