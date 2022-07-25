import json

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

client = MongoClient('localhost', 27017)

Driver = client['CAR_RENTAL_SYSTEM']
Driver_Details = Driver['Driver Details']

Booking = client['CAR_RENTAL_SYSTEM']
Booking_Details = Booking['Booking Details']


######### Finding a particular Driver on the basis of DrivingLicense ###########    

####data2= {"DrivingLicense": "8318536940" }
# n= int (input("enter no of element "))
# d={}

# for i in range(n):
#   key=input ("enter key: ")
#   value= input ("enter value: ")
#   d[key]=value
# print(d)

# def driver_find():
#     result2= str(Driver["Driver Details"].find_one(d))

#     if result2 != "None":
#         print("Driver details found:", result2)
#     else:
#         print("No driver  details found")   
 
 
# driver_find()   



############################# Adding a new driver ########################

# n= int (input("enter no of element "))
# d={}

# for i in range(n):
#   key=input ("enter key: ")
#   value= input ("enter value: ")
#   d[key]=value
# print(d)

# # driver_data = {"DriverID": 12345,"DriverNam": "Root","Email": "root123@google.co.uk","Contact": "925-841-8757"}

# def driver_insert():
#     Driver_Details.insert_one(d)
#     print("Driver Details Added in the database ", d)   

# driver_insert()


###################### Deleting a driver ##########################

# class_list = dict()
# data = input('Enter name & score separated by ":" ')
# temp = data.split(':')
# class_list[temp[0]] = int(temp[1])

# data3= class_list
# print(data3)
# result3= Driver["Driver Details"].delete_many(data3)
# # print(result3)            

# if result3 != "None":
#     print("Driver details deleted:", result3)
# else:
#     print("No driver  details found") 



###### debar a driver when the rating is below a prescribed limit (find all driver with rating above 4)
class_list = dict()
data = input('Enter name & score separated by ":" ')
temp = data.split(':')
class_list[temp[0]] = int(temp[1])

data=class_list

def debar_driver():
    driver_rating = Driver["Driver Details"].find({"AverageRating" : data } )
    
    print("Driver with good rating:",list(driver_rating)) 

    if driver_rating != "None":
        print("Driver details :", driver_rating)
    else:
        print("No driver  details found")    
    for x in driver_rating:
        print(x)

debar_driver()


############################ List of Driver with rides ############################

def driver_list():
    myquery2= Booking_Details.aggregate( [
        {"$group": {
            "_id": {"DriverID": "$DriverID"},
            "uniqueIds": {"$addToSet": "$_id"},
            "count": {"$sum": 1}
            }
        },
        {"$match": { 
            "count": {"$gt": 1}
            }
        },
        {"$sort": {
            "count": -1
            }
        }
    ])

    for x in myquery2:
        print(x)
        
driver_list()




