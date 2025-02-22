import pandas as pd
import os

##################################################
####### Convert haunted_places.csv to .tsv #######
##################################################

# Step 1: Define relative paths
input_file = os.path.join('..', 'data', 'haunted_places.csv')
output_file = os.path.join('..', 'data', 'haunted_places.tsv')

# Step 2: Check if the file exists before attempting to read
if not os.path.exists(input_file):
    print(f"Error: File not found at {os.path.abspath(input_file)}")
    exit(1)

# Step 3: Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)
print(f"File loaded successfully from: {os.path.abspath(input_file)}")

# Step 4: Save the DataFrame as a TSV file
df.to_csv(output_file, sep='\t', index=False)
print(f"File converted successfully: {os.path.abspath(output_file)}")

