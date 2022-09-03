import os

old_class_path = 'labels_test/old.labels'
new_class_path = 'labels_test/new.labels'


"""
map_dict = {old_class_line: new_class_line}
"""
map_dict = {}

with open(new_class_path, 'r') as new_class_f:
    new_classes = new_class_f.readlines()
    with open(old_class_path, 'r') as old_class_f:
        old_classes = old_class_f.readlines()

        for i in range(0, len(old_classes)):
            for j in range(0, len(new_classes)):
                if old_classes[i] == new_classes[j]:
                    map_dict[i] = j
                    break


print(map_dict)