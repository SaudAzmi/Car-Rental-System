import json

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

client = MongoClient('localhost', 27017)
Customer = client['CAR_RENTAL_SYSTEM']
CUstomer_Details = Customer['Customer Details']


with open("C://Users/Saud Azmi/OneDrive/Documents/mongodb/data/customers.json", encoding='utf-8') as f:
    file_data = json.load(f)


Customer_Details_Insert = CUstomer_Details.insert_many(file_data)
client.close()


