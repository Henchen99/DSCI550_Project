import pandas as pd
import os
import re
from number_parser import parse_number
from datefinder import find_dates

##################################################
####### Load and Preprocess Haunted Places #######
##################################################

# Define file paths (assuming relative paths)
data_dir = os.path.join("..", "data", "raw")  # Ensure saving in "raw"
processed_dir = os.path.join("..", "data", "processed")

# Ensure directories exist
os.makedirs(processed_dir, exist_ok=True)

# Define file paths
input_file = os.path.join(data_dir, "haunted_places.tsv")
output_file = os.path.join(processed_dir, "haunted_places_analysis.tsv")

# Check if the file exists
if not os.path.exists(input_file):
    print(f"Error: File not found at {os.path.abspath(input_file)}")
    exit(1)

# Load TSV file
df = pd.read_csv(input_file, sep="\t")
print(f"Loaded dataset: {input_file}")

# Ensure 'description' column exists
if "description" not in df.columns:
    print("Error: 'description' column missing in the dataset.")
    exit(1)

##################################################
################ Feature Engineering #############
##################################################

# Define keywords for feature extraction
audio_keywords = ["noises", "whisper", "footsteps", "screaming", "crying", "voices"]
visual_keywords = ["see", "shadow", "figure", "glowing", "orbs", "apparition", "ghostly"]
witness_keywords = ["witnesses", "people saw", "group saw", "several reported", "locals say"]
apparition_keywords = ["ghost", "spirit", "demon", "angel", "shadow figure", "poltergeist", "ufo", "orb"]
event_keywords = ["murder", "suicide", "accident", "death", "killed", "crime", "hanging"]
time_keywords = {
    "Morning": ["morning", "sunrise", "dawn"],
    "Afternoon": ["afternoon", "midday"],
    "Evening": ["evening", "dusk", "twilight"],
    "Night": ["night", "midnight", "dark"]
}

# Functions to extract features
def contains_keywords(text, keywords):
    """Returns True if any keyword appears in the text."""
    if pd.isna(text):
        return False
    text = text.lower()
    return any(re.search(rf"\b{re.escape(keyword)}\b", text) for keyword in keywords)

def extract_witness_count(text):
    """Extracts witness count from text, detecting both digits and written numbers."""
    if pd.isna(text) or text.strip() == "":
        return 0

    # Extract numbers written as digits (e.g., "3", "20")
    digit_numbers = [int(num) for num in re.findall(r'\b\d+\b', text)]

    # Extract written numbers using parse_number
    word_number = parse_number(text)
    if word_number is not None:
        digit_numbers.append(int(word_number))

    return max(digit_numbers) if digit_numbers else 0  # Return the highest number

def extract_apparition_type(text):
    """Identifies apparition type from description."""
    if pd.isna(text):
        return "Unknown"
    for keyword in apparition_keywords:
        if re.search(rf"\b{re.escape(keyword)}\b", text.lower()):
            return keyword.capitalize()
    return "Unknown"

def extract_event_type(text):
    """Identifies event type from description."""
    if pd.isna(text):
        return "Unknown"
    for keyword in event_keywords:
        if re.search(rf"\b{re.escape(keyword)}\b", text.lower()):
            return keyword.capitalize()
    return "Unknown"

def extract_time_of_day(text):
    """Identifies if the sighting happened in morning, afternoon, evening, or night."""
    if pd.isna(text):
        return "Unknown"
    for time_period, keywords in time_keywords.items():
        if any(re.search(rf"\b{re.escape(keyword)}\b", text.lower()) for keyword in keywords):
            return time_period
    return "Unknown"

def extract_date(text):
    """Extracts date from text using datefinder."""
    if pd.isna(text):
        return None  # Return None instead of a fixed default date
    matches = list(find_dates(text))
    return matches[0].strftime("%Y-%m-%d") if matches else None

##################################################
####### Apply Feature Engineering ################
##################################################

df["Audio_Evidence"] = df["description"].apply(lambda x: contains_keywords(x, audio_keywords))
df["Visual_Evidence"] = df["description"].apply(lambda x: contains_keywords(x, visual_keywords))
df["Witness_Count"] = df["description"].apply(extract_witness_count)
df["Apparition_Type"] = df["description"].apply(extract_apparition_type)
df["Event_Type"] = df["description"].apply(extract_event_type)
df["Time_of_Day"] = df["description"].apply(extract_time_of_day)
df["Haunted_Place_Date"] = df["description"].apply(extract_date)

##################################################
####### Save the Enriched Dataset ################
##################################################

df.to_csv(output_file, sep="\t", index=False)
print(f"Feature engineering completed! Enriched dataset saved at: {output_file}")
