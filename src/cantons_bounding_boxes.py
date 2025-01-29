import requests
import pandas as pd
import json

# List of Swiss cantons
kantons = ['Canton de Vaud', 'Genève', 'Canton de Fribourg',
            'Canton de Berne', 'Canton du Valais', 'Neuchâtel', 'Jura',
            'Kanton Solothurn', 'Kanton Basel-Landschaft',
            'Kanton Basel-Stadt', 'Kanton Aargau', 'Kanton Luzern',
            'Kanton Nidwalden', 'Kanton Obwalden', 'Kanton Zug', 'Kanton Uri',
            'Kanton Schwyz', 'Ticino', 'Kanton Graubünden',
            'Kanton St. Gallen', 'Kanton Zürich', 'Kanton Schaffhausen',
            'Kanton Thurgau', 'Kanton Glarus', 'Kanton Appenzell Ausserrhoden',
            'Kanton Appenzell Innerrhoden']

url = "https://nominatim.openstreetmap.org/search"
headers = {"User-Agent": "Mozilla/5.0"}

def get_cantons_bboxes(list_of_cantons):
    results = []

    for canton in list_of_cantons:
        params = {
            "q": canton, 
            "format": "json",
            "polygon_geojson": 0,
            "addressdetails": 1
        }

        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if data:
            bbox = data[0]["boundingbox"]  # Extract bounding box
            min_lat, max_lat = float(bbox[0]), float(bbox[1])
            min_lon, max_lon = float(bbox[2]), float(bbox[3])

            results.append({
                "Canton": canton,
                "Min_Lat": min_lat,
                "Max_Lat": max_lat,
                "Min_Lon": min_lon,
                "Max_Lon": max_lon
            })

    # Convert to DataFrame
    df = pd.DataFrame(results)
    return df

# Get bounding box data
df_cantons = get_cantons_bboxes(kantons)

# Saving into CSV
df_cantons.to_csv("swiss_cantons_bboxes.csv", index=False)