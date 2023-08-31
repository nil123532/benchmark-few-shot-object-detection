import os

# Set your path to the directory containing the .txt files
path = "/home/nilesh/Benchmark/datasets/BCCD/train_30shot/labels"

# Create a dictionary to store label counts
label_counts = {}

# Loop through each file in the directory
for filename in os.listdir(path):
    if filename.endswith(".txt"):
        with open(os.path.join(path, filename), 'r') as file:
            # Read the file line by line
            for line in file:
                # Split the line into a list (default split is by whitespace)
                elements = line.split()
                # Get the label, which is the first element of the list
                label = elements[0]
                # Increment count in dictionary
                if label in label_counts:
                    label_counts[label] += 1
                else:
                    label_counts[label] = 1

# Print the count of each label
for label, count in label_counts.items():
    print(f"Label {label}: {count} instances")
