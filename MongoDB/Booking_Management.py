import json
from unittest import result

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

client = MongoClient('localhost', 27017)
Booking = client['CAR_RENTAL_SYSTEM']
Booking_Details = Booking['Booking Details']


############# Booking  details based on Customer ID:################
# n= int (input("enter no of element "))
# d={}

# for i in range(n):
#   key=input ("enter key: ")
#   value= input ("enter value: ")
#   d[key]=value
# print(d)

# ## car_d= {"CarID": "1FTSX2A56AE727901" }
# result2= Booking_Details.find(d)
            

# if result2 != "None":
#     print("Booking details found:", list(result2))
# else:
#     print("No Car Booking details found")
    
###################### Booking  details based on Booking ID:################
# class_list = dict()
# data = input('Enter name & score separated by ":" ')
# temp = data.split(':')
# class_list[temp[0]] = int(temp[1])
# data=class_list

# ## car_d= {'BookingID': 2}
# def bookid_check():
#     result2= Booking_Details.find(data)


#     if result2 != "None":
#         print("Booking details found:", list(result2))
#     else:
#         print("No Car Booking details found")    

# bookid_check()
############# Booking  details based on Driver ID:################

##car_d= {'DriverID': 11}
# class_list = dict()
# data = input('Enter name & score separated by ":" ')
# temp = data.split(':')
# class_list[temp[0]] = int(temp[1])

            
# def bookcheck_Did():
#     data1=class_list
#     result2= Booking_Details.find(data1)
#     if result2 != "None":
#         print("Booking details found:", list(result2))
#     else:
#         print("No Car Booking details found")  

# bookcheck_Did()
################## Updating booking details #####################
class_list = dict()
data = input('Enter name & score separated by ":" ')
temp = data.split(':')
class_list[temp[0]] = int(temp[1])


n= int (input("enter no of element "))
d={}

for i in range(n):
  key=input ("enter key: ")
  value= input ("enter value: ")
  d[key]=value
print(d)

data2=class_list

result123=Booking_Details.find_one_and_update (data2,
                            {"$set":
                                    d
                            },upsert=True)
print(result123)

# {"DropLatitude": 124.754346}
