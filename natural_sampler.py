import os
import shutil
import random
import numpy as np
from collections import defaultdict

#set random seed
random.seed(0)
np.random.seed(0)
# Given directory path
label_dir = "/home/nilesh/Benchmark/datasets/BCCD/train/labels"
image_dir = "/home/nilesh/Benchmark/datasets/BCCD/train/images"

# Create output directories for sampled images and labels
sampled_label_dir = "/home/nilesh/Benchmark/datasets/BCCD/train_10shot/labels"
sampled_image_dir = "/home/nilesh/Benchmark/datasets/BCCD/train_10shot/images"

os.makedirs(sampled_label_dir, exist_ok=True)
os.makedirs(sampled_image_dir, exist_ok=True)

# All available label files
all_label_files = [f for f in os.listdir(label_dir) if os.path.isfile(os.path.join(label_dir, f))]

# Step 1: Sample an initial dataset
dlen = 30  # Number of samples
samples = set(np.random.choice(all_label_files, dlen, replace=False))

# Get classes present in each label file
def get_classes(file):
    with open(os.path.join(label_dir, file), 'r') as f:
        return [int(line.split()[0]) for line in f.readlines()]

# Create a mapping of class to label files
class_to_samples_map = defaultdict(set)
sampled_class_to_samples_map = defaultdict(set)

for file in all_label_files:
    for cls in get_classes(file):
        class_to_samples_map[cls].add(file)

for file in samples:
    for cls in get_classes(file):
        sampled_class_to_samples_map[cls].add(file)

# Step 2: Guarantee at least 1-shot for each class
new_samples = set()
keep_samples = set()

max_class_id = 3  # Placeholder
for class_id in range(max_class_id):
    if class_id not in sampled_class_to_samples_map:
        idx = random.choice(list(class_to_samples_map[class_id]))
        new_samples.add(idx)
    else:
        idx = random.choice(list(sampled_class_to_samples_map[class_id]))
        keep_samples.add(idx)

# Step 3: Update the samples
if new_samples:
    del_samples = set(np.random.choice(list(samples - keep_samples), len(new_samples), replace=False))
    samples -= del_samples
    samples |= new_samples

print(samples)
print(len(samples))
class_counts = defaultdict(int)

for file in samples:
    for cls in get_classes(file):
        class_counts[cls] += 1

# Print the class counts
for class_id, count in class_counts.items():
    print(f"Class {class_id}: {count} instances")
class_image_counts = defaultdict(int)

for file in samples:
    label_file_path = os.path.join(label_dir, file)
    image_file_name = file.replace(".txt", ".jpg")  # Replace with your actual image extension
    image_file_path = os.path.join(image_dir, image_file_name)

    # Move label files
    shutil.copy(label_file_path, os.path.join(sampled_label_dir, file))
    
    # Move image files
    shutil.copy(image_file_path, os.path.join(sampled_image_dir, image_file_name))
