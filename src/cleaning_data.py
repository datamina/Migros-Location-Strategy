import json
import pandas as pd
import glob
import os

######### prep list with all files names

def list_of_files(folder_name):

    file_list = glob.glob(f"../data/{folder_name}/*.json")
    file_list = [os.path.basename(file) for file in file_list]
    return file_list


######### concat_and_clean

def concat_and_clean(shop_name):

    def list_of_files(shop_name):

        file_list = glob.glob(f"../data/{shop_name}/*.json")
        file_list = [os.path.basename(file) for file in file_list]
        return file_list
    
    file_list = list_of_files(shop_name)
    
    all_data = pd.DataFrame()       # empty df to be filled

    for file_name in file_list:         #load content into DFs
        with open(f"../data/{shop_name}/{file_name}", "r", encoding="utf-8") as file:      
            data = json.load(file)

        # Convert to a DF and concat
        df = pd.DataFrame(data)
        all_data = pd.concat([all_data, df], ignore_index=True)

    # clean
    all_data = all_data.drop(columns = ['icon','icon_background_color','icon_mask_base_uri','photos','reference','place_id','plus_code','opening_hours','business_status'])
    all_data["postal_code"] = all_data["formatted_address"].str.extract(r'(\b\d{4}\b)')
    all_data["city"] = all_data["formatted_address"].str.extract(r'\b\d{4}\b\s([\w-]+)')

    return all_data


migros_all_cleaned = concat_and_clean('Migros')
print(migros_all_cleaned.head())