import json
import pymongo
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from pymongo import ReturnDocument

client = MongoClient('localhost', 27017)
Customer = client['CAR_RENTAL_SYSTEM']
CUstomer_Details = Customer['Customer Details']


########################### Finding a particular Customer on the basis of Customer_ID ##########################
class_list = dict()
data = input('Enter name & score separated by ":" ')
temp = data.split(':')
class_list[temp[0]] = int(temp[1])

print (class_list)
##### function to display customer details########
def cust():
  data1= class_list
  result= str(Customer["Customer Details"].find_one(data1)
            )
  if result != "None":
    print("Customer you are looking for is :", result)
  else:
    print("Unknown CustomerID")

cust()
# ############################ Adding a new customer ##############################
n= int (input("enter no of element "))
d={}

for i in range(n):
  key=input ("enter key: ")
  value= input ("enter value: ")
  d[key]=value
print(d)

# # my_data = {"CustomerID": 12345,"CustomerName": "Root","Email": "root123@google.co.uk","Contact": "925-841-8757"}
def Add_cust():
    CUstomer_Details.insert_one(d)
    print("Customer Details Added in the database ", d) 


Add_cust()



################### Updating the customer details##########################
class_list = dict()
data = input('Enter name & score separated by ":" ')
temp = data.split(':')
class_list[temp[0]] = int(temp[1])

def Cust_update():
    cust_result= str(Customer["Customer Details"].find_one(class_list))
    print(cust_result)

    if cust_result != "None":
        update_cust_details= CUstomer_Details.find_one_and_update(class_list,
                                {"$set":
                                        {"Email": "test12@gmail.com"}}
                                ,upsert=True)
                                
    else:
        print("No customer found")  
    cust_result1= str(Customer["Customer Details"].find_one(class_list))
    print(cust_result1)

Cust_update()


