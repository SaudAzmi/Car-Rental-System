import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
Driver = client['CAR_RENTAL_SYSTEM']
Driver_Details = Driver['Driver Details']

with open("C://Users/Saud Azmi/OneDrive/Documents/mongodb/data/drivers.json", encoding='utf-8') as f:
    file_data = json.load(f)

Driver_Details.insert_many(file_data)


client.close()