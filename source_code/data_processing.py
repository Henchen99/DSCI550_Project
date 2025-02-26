import pandas as pd
import os

##################################################
####### Convert haunted_places.csv to .tsv #######
##################################################

# Step 1: Define relative paths
data_dir = os.path.join('..', 'data', 'raw')  # Save to "raw" inside "data"

# Ensure the directory exists
os.makedirs(data_dir, exist_ok=True)

# Define file paths
input_file = os.path.join('..', 'data', 'raw', 'haunted_places.csv')  # Assuming CSV is also in "raw"
output_file = os.path.join(data_dir, 'haunted_places.tsv')

# Step 2: Check if the file exists before attempting to read
if not os.path.exists(input_file):
    print(f"Error: File not found at {os.path.abspath(input_file)}")
    exit(1)

# Step 3: Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)
print(f"File loaded successfully from: {os.path.abspath(input_file)}")

# Step 4: Save the DataFrame as a TSV file inside "raw"
df.to_csv(output_file, sep='\t', index=False)
print(f"File converted successfully: {os.path.abspath(output_file)}")

##################################################
# generate a list of city,country, state, and state_abbrev
##################################################
# Step 1: Define relative paths
data_dir = os.path.join('..', 'data', 'raw')  # Save to "raw" inside "data"
# Ensure the directory exists
os.makedirs(data_dir, exist_ok=True)
# Define file paths
input_file = os.path.join('..', 'data', 'raw', 'haunted_places.csv')  # Assuming CSV is also in "raw"
output_file = os.path.join(data_dir, 'haunted_places_list.csv')
# Step 2: Check if the file exists before attempting to read
if not os.path.exists(input_file):
    print(f"Error: File not found at {os.path.abspath(input_file)}")
    exit(1)
# Step 3: Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)
print(f"File loaded successfully from: {os.path.abspath(input_file)}")
# Step 4: Save the DataFrame as a CSV file inside "raw"
df = df[['city', 'country', 'state', 'state_abbrev']]
df.to_csv(output_file, index=False)
print(f"File converted successfully: {os.path.abspath(output_file)}")
