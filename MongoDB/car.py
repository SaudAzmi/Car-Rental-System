import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
Car = client['CAR_RENTAL_SYSTEM']
Car_Details = Car['Car Details']

with open("C://Users/Saud Azmi/OneDrive/Documents/mongodb/data/car_new.json", encoding='utf-8') as f:
    file_data = json.load(f)

Car_Details.insert_many(file_data)


client.close()