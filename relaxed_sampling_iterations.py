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
                relaxed = 0  # Initialize the relaxed variable
                all_sampled_files = set()  # To keep track of files that have been sampled
                iterations = 0

                while True:
                    iterations += 1
                     # Progressively relax both upper and lower limits
                    upper_limit = shots + relaxed
                    lower_limit = max(1, shots - relaxed)  # Lower limit should not go below 1

                    #potential_files = random.sample(list(label_img_files.keys()), min(shots - sample_shots, len(label_img_files)))
                    potential_files = random.sample(list(label_img_files.keys()), shots)
                    for file in potential_files:
                        if file not in sample_files:
                            temp = label_img_files[file]  # Let's say this is the number of shots for the current file
                            all_sampled_files.add(file)  # Mark this file as considered
                            if (sample_shots + temp > upper_limit) or (sample_shots + temp < lower_limit):
                                continue

                             # Add this file to the sampled files and update the number of shots
                            sample_files.append(file)
                            sample_shots += temp

                            # Check if we reached the number of shots
                            if (sample_shots <= upper_limit) and (sample_shots >= lower_limit):
                                break

                     # If we have reached the number of shots, exit
                    if (sample_shots <= upper_limit) and (sample_shots >= lower_limit):
                        break
                    #if iterations/10,000 = 0 relax
                    if (iterations%100000) == 0 :
                        relaxed += 1

                     # If we've gone through all the potential files, then relax the constraint
                    #if len(all_sampled_files) == len(label_img_files.keys()):
                     #   relaxed += 1/(shots*shots)  # Increase the relaxation factor
                      #  all_sampled_files = set()
                        #print("Relaxed!")
       

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
