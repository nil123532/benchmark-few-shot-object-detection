import os
import random
import shutil

label_dir = '/home/nilesh/few-shot-coco/JSON2YOLO/novel_labels/labels/novel_set1/'
train_dir = 'train_novel/labels/'
other_dir = 'val_novel/labels/'
os.makedirs(train_dir, exist_ok=True)
os.makedirs(other_dir, exist_ok=True)

file_list = os.listdir(label_dir)
random.shuffle(file_list)

label_counts = {}

for filename in file_list:
    with open(label_dir + filename, 'r') as f:
        lines = f.readlines()
    labels_in_file = [int(line.split()[0]) for line in lines]
    temp_label_counts = label_counts.copy()

    for label in labels_in_file:
        temp_label_counts[label] = temp_label_counts.get(label, 0) + 1

    if all(count <= 30 for count in temp_label_counts.values()):
        # If adding this file doesn't exceed 30 instances for any label, use it
        shutil.copy(label_dir + filename, train_dir + filename)
        label_counts = temp_label_counts
    #else:
        # Otherwise, put the file in the other directory
        #shutil.copy(label_dir + filename, other_dir + filename)
