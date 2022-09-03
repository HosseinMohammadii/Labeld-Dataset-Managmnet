import os
from os import listdir
from os.path import isfile, join
import shutil

base_input_dir = "/home/hossein/yolo/finalV2-3"
train_dir = "train"
valid_dir = "valid"



with open(os.path.join(base_input_dir, 'train.txt'), 'w') as train_text_file:
    train_files_list = listdir(os.path.join(base_input_dir, train_dir))
    train_files_list.sort()
    for f_name in train_files_list:
        if f_name.endswith('jpg'):
            train_text_file.write(os.path.join(train_dir, f_name)+'\n')


with open(os.path.join(base_input_dir, 'valid.txt'), 'w') as valid_text_file:
    valid_files_list = listdir(os.path.join(base_input_dir, valid_dir))
    valid_files_list.sort()
    for f_name in valid_files_list:
        if f_name.endswith('jpg'):
            valid_text_file.write(os.path.join(valid_dir, f_name)+'\n')

