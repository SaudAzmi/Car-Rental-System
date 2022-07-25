import json

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

client = MongoClient('localhost', 27017)
Service_centre = client['CAR_RENTAL_SYSTEM']
Service_centre_Details = Service_centre['Service_centre_D']



with open("C://Users/Saud Azmi/OneDrive/Documents/mongodb/data/Service_centre.json", encoding='utf-8') as f:
    file_data = json.load(f)


Service_centre_Details_Insert = Service_centre_Details.insert_many(file_data)
client.close()




