import json

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

client = MongoClient('localhost', 27017)
Booking = client['CAR_RENTAL_SYSTEM']
Booking_Details = Booking['Booking Details']


with open("C://Users/Saud Azmi/OneDrive/Documents/mongodb/data/booking.json", encoding='utf-8') as f:
    file_data = json.load(f)


Booking_Details_Insert = Booking_Details.insert_many(file_data)
client.close()
