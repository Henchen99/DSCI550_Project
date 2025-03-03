import pandas as pd

hp_df = pd.read_csv("../raw/haunted_places.csv")
from transformers import pipeline
pipe = pipeline("text-generation", model="Qwen/Qwen2.5-32B-Instruct",device_map="auto")

def date_extraction(description):
    prompt = """
        The text below is a description of a haunted location.\n
        Please extract out the date that the haunted location is dated to with the format: Month-Day-Year\n
        If no date is mentioned, then put 'N/A' as your output.\n
        If part of the date is mentioned, put the dates available with 00 as filler for the other values.\n
        Please output your final result after: #### 

        For example:\n
        Description: "The house dated back to the 20th century", output: #### 01-01-1900\n
        Description: "The location was discovered in May of 1854", output: #### 05-01-1854\n
        Description: "If you take the road towards the beach, you will come to a gravel road leading north", output: #### N/A\n
        \n\n
        Description:\n
    """
    messages = [
        {"role": "user", "content": prompt + description},
    ]
    llama_output = pipe(messages)[0]['generated_text'][1]['content']
    final_date = llama_output.split("####")[-1].strip()
    # print(f"final_date: {final_date}")
    return final_date


def witness_count_extraction(description):
    prompt = """
        The text below is a description of a haunted location.\n
        Please extract out the witness count from the haunted location.\n
        If no witness count is mentioned, then put 'N/A' as your output.\n
        Please output your final result after: #### 

        For example:\n
        Description: "A mysterious figure was seen by 3 eye witnesses", output: #### 3\n
        Description: "People said they heard voices", output: #### N/A\n
        \n\n
        Description:\n
    """
    messages = [
        {"role": "user", "content": prompt + description},
    ]
    llama_output = pipe(messages)[0]['generated_text'][1]['content']
    final_witness_count = llama_output.split("####")[-1].strip()
    # print(f"final_witness_count: {final_witness_count}")
    return final_witness_count


haunted_place_date_list = []
witness_count_list = []
for index, row in hp_df.iterrows():
    if index<10:
        print(f"index: {index}")
    date = date_extraction(row['description'])
    witness_count = witness_count_extraction(row['description'])
    haunted_place_date_list.append(date)
    witness_count_list.append(witness_count) 
print(len(haunted_place_date_list), len(witness_count_list))
hp_df['HP_date'] = haunted_place_date_list
hp_df['Witness_count'] = witness_count_list

print(hp_df.head(1))

hp_df.to_csv("../processed/hp_with_date_and_witness_count.csv", index=False)
