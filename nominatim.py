import json
import requests
import time
import os

class Shops:
    def __init__(self, shop):
        self.shop = shop

    # OpenStreetMap Nominatim API URL (No API Key Required)
    url = "https://nominatim.openstreetmap.org/search"

    def get_shops_per_canton(self):

        # List copy pasted from pgeocode (jobs.ch exercise)
        kantons = ['Canton de Vaud']  
        """
        , 'Genève', 'Canton de Fribourg',
            'Canton de Berne', 'Canton du Valais', 'Neuchâtel', 'Jura',
            'Kanton Solothurn', 'Kanton Basel-Landschaft',
            'Kanton Basel-Stadt', 'Kanton Aargau', 'Kanton Luzern',
            'Kanton Nidwalden', 'Kanton Obwalden', 'Kanton Zug', 'Kanton Uri',
            'Kanton Schwyz', 'Ticino', 'Kanton Graubünden',
            'Kanton St. Gallen', 'Kanton Zürich', 'Kanton Schaffhausen',
            'Kanton Thurgau', 'Kanton Glarus', 'Kanton Appenzell Ausserrhoden',
            'Kanton Appenzell Innerrhoden']
        """

        for canton in kantons:
            canton_stores = []

            params = {
                "q": f"{self.shop} in {canton}",
                "format": "json",  
                "addressdetails": 1,
                "limit": 40,  # Get up to 50 results
            }
            
            # Send request
            try:
                req = requests.get(Shops.url, params=params, headers={"User-Agent": "Mozilla/5.0"})
                data = req.json()
                ###### check pagination doc
                print(headers)
                print(f"Response for {canton}: {len(data)} results found")

                # Store results
                canton_stores.extend(data)

                # Wait between requests (to avoid rate limits)
                time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for {canton}: {e}")
                continue

            # Save to JSON file inside `.data` folder
            os.makedirs(".data", exist_ok=True)  # Ensure directory exists
            file_path = f".data/{self.shop}_stores_in_{canton}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(canton_stores, f, indent=4, ensure_ascii=False)

            print(f"Saved {len(canton_stores)} results to {file_path}")

shop_scraper = Shops("supermarket")
shop_scraper.get_shops_per_canton()