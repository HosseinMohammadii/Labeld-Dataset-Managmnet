import os
from os import listdir
from os.path import isfile, join
import shutil

# from roboflow alphabet sorted to gtsdb sequence

# class_map = {
#     0: 31, 1: 25, 2: 29, 3: 18, 4: 13, 5: 34,
#     6: 37, 7: 33, 8: 36, 9: 35, 10: 39,
#     11: 38, 12: 17, 13: 9, 14: 10, 15: 15,
#     16: 16, 17: 11, 18: 12, 19: 32, 20: 42,
#     21: 41, 22: 6, 23: 24, 24: 40, 25: 28,
#     26: 23, 27: 30, 28: 7, 29: 8, 30: 1,
#     31: 2, 32: 3, 33: 4, 34: 5, 35: 14,
#     36: 26, 37: 22,
# }

old_class_path = '/home/hossein/yolo/final/obj.labels'
new_class_path = '/home/hossein/yolo/final2/obj.names'


"""
class_map = {old_class_line: new_class_line}
"""
class_map = {}

with open(new_class_path, 'r') as new_class_f:
    new_classes = new_class_f.readlines()
    with open(old_class_path, 'r') as old_class_f:
        old_classes = old_class_f.readlines()

        for i in range(0, len(old_classes)):
            for j in range(0, len(new_classes)):
                if old_classes[i] == new_classes[j]:
                    class_map[i] = j
                    break

# print(old_classes)
# print(new_classes)
l = sorted(class_map.items(), key=lambda x: x[1])
print(l)

base_input_dir = "/home/hossein/yolo/final/train"

base_output_dir = "/home/hossein/yolo/final2/train"


def fix_name(old_name: str, file_type) -> str:
    return old_name[:11] + '.' + file_type


def change_txt_file_classes(inputs_lines: iter) -> list:
    edited_lines = []
    for line in inputs_lines:
        phrases = line.split(' ')
        try:
            if phrases[0] in ['None', 'NONE', 'none']:
                print(phrases)
                continue
            phrases[0] = str(class_map[int(phrases[0])])
            edited_lines.append(' '.join(phrases))
        except Exception:
            pass
    return edited_lines

i = 1

print(base_input_dir, '\nto\n', base_output_dir)
files_list = listdir(base_input_dir)
# files_list = files_list[:10]

for f_name in files_list:
    if f_name.endswith('.txt'):
        with open(os.path.join(base_input_dir, f_name), 'r') as f:
            new_lines = change_txt_file_classes(f.readlines())
            if len(new_lines) == 0:
                continue
            with open(os.path.join(base_output_dir, f_name), 'w') as new_f:
                new_f.writelines(new_lines)

            img_name = f_name.replace('.txt', '.jpg')
            shutil.copyfile(os.path.join(base_input_dir, img_name),
                            os.path.join(base_output_dir, img_name))

    i += 1
    if i % 50 == 0:
        print(i, 'files processed.')



