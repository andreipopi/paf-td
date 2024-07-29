import os
import subprocess
import re

# Specify the folder containing the instance files and the encoding file
folder_path = '/Users/andrei/Documents/GitLab/praaf-tree-decomposition/Experiments/instance-set/generated_instances_asp_dense_uncertain'  # Replace with the path to your folder
encoding_file = 'preprocess_simple.lp'  # Replace with the path to your encoding file

# List to hold results
results = []

# Regex pattern to extract k and n from filename
pattern = re.compile(r'k(\d+)_n(\d+)_')

# Iterate over all files in the given folder
for filename in os.listdir(folder_path):
    instance_file = os.path.join(folder_path, filename)
    # Build the clingo command
    command = ['clingo', encoding_file, instance_file]
    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Parse the output to count in() and out() occurrences
    output = result.stdout
    in_count = output.count('in(')
    out_count = output.count('out(')
    
    # Extract k and n from filename using regex
    match = pattern.search(filename)
    if match:
        k = int(match.group(1))
        n = int(match.group(2))
        # Append results to list
        results.append((k, n, filename, in_count, out_count))

# Sort results by k and then by n
results.sort()

# Print sorted results
for result in results:
    k, n, filename, in_count, out_count = result
    print(filename, ",", in_count, ",", out_count)