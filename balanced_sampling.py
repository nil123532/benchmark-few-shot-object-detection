import random
import glob
import os
import shutil

def generate_seeds():
    classes = [0, 1, 2]  # Define your classes

    for seed in range(1, 10):  # Loop through the seeds
        random.seed(seed)

        for label in classes:  # Loop through each class
            label_img_files = {}  # Dictionary to hold image filenames for each label

            # Populate the list with instances of each class
            for file in glob.glob("/home/nilesh/Benchmark/datasets/BCCD/train/labels/*.txt"):
                count = 0
                with open(file, 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if int(parts[0]) == label:
                        count += 1
                if count > 0:
                    label_img_files[file] = count

            # Now let's sample exactly 'shots' instances for each class
            for shots in [1, 2, 3, 5, 10, 30]:
                sample_files = []
                sample_shots = 0

                while True:
                    #potential_files = random.sample(list(label_img_files.keys()), min(shots - sample_shots, len(label_img_files)))
                    potential_files = random.sample(list(label_img_files.keys()), shots)

                    for file in potential_files:
                        if file not in sample_files:
                            if sample_shots + label_img_files[file] > shots:
                                continue
                            sample_files.append(file)
                            sample_shots += label_img_files[file]

                        if sample_shots == shots:
                            break

                    if sample_shots == shots:
                        break

                # Create directory to save sampled files
                save_dir = get_save_path_seeds(shots, seed)
                os.makedirs(save_dir, exist_ok=True)

                # Copy sampled files to the new directory
                for file in sample_files:
                    shutil.copy(file, save_dir)

def get_save_path_seeds(shots, seed):
    prefix = f"{shots}shot_seed{seed}"
    save_dir = os.path.join("/home/nilesh/Benchmark/datasets/BCCD", prefix)
    return save_dir

# Generate seeds
generate_seeds()
