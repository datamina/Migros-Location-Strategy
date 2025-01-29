import json
import requests
import time

class Shops:
    def __init__(self, shop):
        self.shop = shop
        
    api_key = json.load(open("googlemaps_key.json"))["api_key"]
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

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
                "query": f"{self.shop} in {canton}",
                "key": Shops.api_key
        }
            i=0

            while i <= 20:
                req = requests.get(Shops.url, params=params)
                data = req.json()
                print(f"Response for {canton}: {data.get('status')}")

                if data.get('status') != 'OK':
                    print(data)

                # Add results
                if "results" in data:
                    canton_stores.extend(data["results"]) #not using append or will nest results

                # Check for next page token
                next_page_token = data.get("next_page_token")
                if not next_page_token:
                    break 

                # Update params for next request
                params["pagetoken"] = next_page_token

                time.sleep(10)

                i+=1

            # Saving into JSON
            with open(f"../tmp/{self.shop}_stores_in_{canton}.json", 'w') as f:
                json.dump(canton_stores, f, indent=4)

        print(f"Total results: {len(canton_stores)}")
        
