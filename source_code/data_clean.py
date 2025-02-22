import pandas as pd
import os

# Step 1: Define relative paths
# Navigate up one level to access the 'data' folder
input_file = os.path.join('..', 'data', 'haunted_places.csv')  # Correct relative path
output_file = os.path.join('..', 'data', 'haunted_places.tsv')  # Output TSV file in the same folder

# Debugging: Print the full path to verify
print(f"Looking for input file at: {os.path.abspath(input_file)}")

# Step 2: Read the CSV file into a pandas DataFrame
try:
    df = pd.read_csv(input_file)
    print("File loaded successfully!")
except FileNotFoundError:
    print(f"Error: File not found at {os.path.abspath(input_file)}")
    exit(1)

# Step 3: Save the DataFrame as a TSV file
df.to_csv(output_file, sep='\t', index=False)

print(f"File converted successfully: {output_file}")
