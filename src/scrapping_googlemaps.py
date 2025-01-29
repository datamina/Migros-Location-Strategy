import json
import requests
import time
from src.canton_stores_retrieving import Shops

migros_instance = Shops("Migros")
migros_instance.get_shops_per_canton()

"""
coop_instance = Shops("Coop")
coop_instance.get_shops_per_canton()

aldi_instance = Shops("Aldi")
aldi_instance.get_shops_per_canton()

lidl_instance = Shops("Lidl")
lidl_instance.get_shops_per_canton()

denner_instance = Shops("Denner")
denner_instance.get_shops_per_canton()
"""