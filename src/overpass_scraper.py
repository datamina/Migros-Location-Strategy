import json
import requests
import time
import os
import pandas as pd

class Shops:
    def __init__(self, shop):
        self.shop = shop
        self.url = "http://overpass-api.de/api/interpreter"
        
        # Load canton bounding boxes from CSV
        df = pd.read_csv("swiss_cantons_bboxes.csv")
        self.canton_bboxes = pd.Series(df[["Min_Lon", "Min_Lat", "Max_Lon", "Max_Lat"]].values.tolist(), index=df["Canton"]).to_dict()

    def get_shops_per_canton(self):
        os.makedirs("./tmp", exist_ok=True)  # Create folder if not exists

        for canton, bbox in self.canton_bboxes.items():
            print(f"Searching for '{self.shop}' in {canton}...")

            # Overpass Query (search for "shop=supermarket" or "name=self.shop")
            query = f"""
            [out:json][timeout:50];
            (
                node["shop"="{self.shop}"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
                way["shop"="{self.shop}"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
                relation["shop"="{self.shop}"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
            );
            out center;
            """

            # Make request to Overpass API
            try:
                response = requests.get(self.url, params={"data": query})
                response.raise_for_status()  # Check if request was successful
                data = response.json()

                # Extract results
                stores = []
                for element in data.get("elements", []):
                    store_info = {
                        "id": element.get("id"),
                        "name": element.get("tags", {}).get("name", "Unknown"),
                        "address": element.get("tags", {}).get("addr:street", "Unknown"),
                        "postcode": element.get("tags", {}).get("addr:postcode", "Unknown"),
                        "city": element.get("tags", {}).get("addr:city", "Unknown"),
                        "lat": element.get("lat") if "lat" in element else element.get("center", {}).get("lat"),
                        "lon": element.get("lon") if "lon" in element else element.get("center", {}).get("lon"),
                    }
                    stores.append(store_info)

                # Save to JSON
                with open(f"./tmp/{self.shop}_stores_in_{canton}.json", 'w') as f:
                    json.dump(stores, f, indent=4)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for {canton}: {e}")
            time.sleep(1)  

supermarket = Shops('supermarket')
supermarket.get_shops_per_canton()