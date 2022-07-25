# import json
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)

Service_centre = client['CAR_RENTAL_SYSTEM']
Service_centre_Details = Service_centre['Service_centre_D']



client1 = MongoClient('localhost', 27017)
Car = client1['CAR_RENTAL_SYSTEM']
Car_Details = Car['Car Details']


# #################################### Adding New car ########################################
# n= int (input("enter no of element "))
# d={}
# for i in range(n):
#   key=input ("enter key: ")
#   value= input ("enter value: ")
#   d[key]=value
# print(d)
# # Car_data = {"RegNo":"4E7MP2ET3AG031221","Manufacturer":"NEXON","CarModel":"Sunrise","YearOfPurchase":2010,"Availability":"true"}
# def add_car():
# 	Car_Details.insert_one(d)
# 	print("Car Details Added into the database ", d) 
# add_car()

# ################################# List of Car which are available for ride #################################
# # list_of_car= {"Availability":"AVAILABLE" }
# n= int (input("enter no of element "))
# d={}

# for i in range(n):
#   key=input ("enter key: ")
#   value= input ("enter value: ")
#   d[key]=value
# print(d)

# def car_list():
# 	result2= Car['Car Details'].find(d)


# 	if result2 != None:
# 		print("Car details found:", list(result2))
# 	else:
# 		print("No car  details found")  
# car_list()


############################## car health#####################################

myquery= Service_centre_Details.aggregate( [  
    {
        "$project":
        {
            "Car_id":1,
            "service_id":1,
            "maintenance_date" :1,
            "dtDiff2": {"$subtract": [{"$toLong":{"$round": {"$divide": [{ "$subtract": ["$$NOW", "$maintenance_date"] }, 
                                                                         86400000] }}},{"$toLong":150}]},

            "status":
                    {
                    "$cond":{"if":{"$gte": [{"$toLong":{"$round": { "$divide": [{ "$subtract": ["$$NOW","$maintenance_date"] }, 
                                                                                    86400000] }}},{"$toLong":150}]},
                                 "then":"Need Service","else" : "Good"}
                    }

        }
    }
])
for x in myquery:
  print(x)

 
########################## Car Service History details#########################
# n= int (input("enter no of element "))
# d={}

# for i in range(n):
#   key=input ("enter key: ")
#   value= input ("enter value: ")
#   d[key]=value
# print(d)

# def Car_hist():
#     # data2= {'Car_id': '3C3CFFDR2FT212065'}
#     result2= Service_centre_Details.find(d)
                

#     if result2 != "None":
#         print("Car Service details found:", list(result2))
#     else:
#         print("No Car Service  details found")

# Car_hist()
