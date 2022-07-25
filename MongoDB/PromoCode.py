import json

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

client = MongoClient('localhost', 27017)
Booking = client['CAR_RENTAL_SYSTEM']
Booking_Details = Booking['Booking Details']

Driver = client['CAR_RENTAL_SYSTEM']
Driver_Details = Driver['Driver Details']

########################Customer Discount ############################

# n = int(input("Enter number  : ")) 
 
# Query= [{
# 		"$project":
# 		{
# 			"CustomerID": 1,
# 			"Customer_Rating":1,
# 			"status":{
# 				'$cond':{
# 					"if":{"$gte":["$Customer_Rating",n]},
# 					"then" :"20 percent off",
# 					"else" : "10 percent off"
# 					}
# 					}
# 		}
# 	}]

# cursor = Booking_Details.aggregate(Query)
# for doc in cursor:
#         print(doc)


########################## Bonus for Drivers ##################


d = int(input("Enter number  : ")) 
myquery2= Driver_Details.aggregate( [{
	"$project":
	{
		"DriverID": 1,
		"status":{
			'$cond':{
				"if":{"$gte":["$AverageRating",d]},
				"then" :"10 percent bonus",
				"else" : "4 percent bonus"
				}
				}
	}
}])

for x in myquery2:
  print(x)