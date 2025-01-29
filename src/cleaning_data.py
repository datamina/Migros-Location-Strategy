import json
import pandas as pd
import glob #finds all the pathnames matching a specified pattern 
import os

######### prep list with all files names

# Function to list all JSON files in a folder
def list_of_files(folder_name):
    file_list = glob.glob(f"./{folder_name}/*.json")
    file_list = [os.path.basename(file) for file in file_list]
    return file_list


######### concat_and_clean

def concat_and_clean(file_list):
    all_data = pd.DataFrame()  # Empty df to be filled

    for file_name in file_list:  # Load content into DFs
        file_path = f"./tmp/{file_name}"  # Corrected file path
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Convert to a DF and concat
        df = pd.DataFrame(data)
        all_data = pd.concat([all_data, df], ignore_index=True)

    # Optional cleaning: Uncomment and adjust this as needed
    # all_data = all_data.drop(columns=['icon', 'icon_background_color', 'icon_mask_base_uri', 'photos', 'reference', 'place_id', 'plus_code', 'opening_hours', 'business_status'])
    # all_data["postal_code"] = all_data["formatted_address"].str.extract(r'(\b\d{4}\b)')
    # all_data["city"] = all_data["formatted_address"].str.extract(r'\b\d{4}\b\s([\w-]+)')

    return all_data


# Get file names
files = list_of_files('tmp')
# Combine data from the files
data = concat_and_clean(files)
data.to_csv("output.csv", index=False)  # Optionally save to CSV

print(data.info())
df = data
#print(sorted(df['name'].unique()))

df = df[df['name'] != 'Unknown']

df = df[(df['postcode'] != 'Unknown') | (df['city'] != 'Unknown')]  # Keep rows where either 'postcode' or 'city' is not 'Unknown'

print(df.info())
print(df.head())  # Print the first few rows of the cleaned data
