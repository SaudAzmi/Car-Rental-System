import json

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

client = MongoClient('localhost', 27017)
DB = client['CAR_RENTAL_SYSTEM']
collection_neighborhood_Details = DB['neighborhood Details']
collection_carservicecentre_Details=DB['carservicecentre Details']

########## Determining the user's current neighborhood using $geoIntersects
############ Show the number of car service centre in that neighborhood using $geoWithin
############# Find car service centre within a specified distance of the user using $nearSphere.

# #collection_neighborhood_Details.insert_many(file_nh)
# collection_carservicecentre_Details.insert_many(file_sc_data)

#####################finding collection###########################
# for doc1 in collection_neighborhood_Details.find({}):
#       print(doc1)
# for doc2 in collection_carservicecentre_Details.find({}):
#       print(doc2)

############################ Find one detail##########################
# result2= str(collection_carservicecentre_Details.find_one())

# if result2 != "None":
#     print("Details found:", result2)
# else:
#     print("Details found")

# result3= str(collection_neighborhood_Details.find_one())

# if result3 != "None":
#     print("details found:", result3)
# else:
#     print("details found")

#######################Find the Current Neighborhood#############################

# query=collection_neighborhood_Details.find_one({ "geometry": { "$geoIntersects": { "$geometry": { "type": "Point", "coordinates": [ -73.94322686012315,40.701520709145726 ] } } } })
# print(query)


############all Car_service_centre within five miles of the user:
######use $geoWithin with $centerSphere. 
# $centerSphere is a  syntax to denote a circular region by specifying the center and the radius in radians.
####3963.2 is radius of earth in Miles.

# number=int(input("Enter number  : ")) 
# radius=3963.2
# Query2= collection_carservicecentre_Details.find({ "location":
#    { "$geoWithin":
#       { "$centerSphere": [ [ -73.93414657, 40.82302903 ], number / radius ] } } })

# print(list(Query2))

##########All car service within five miles of the user in sorted order from nearest to farthest#########

query3=collection_carservicecentre_Details.find({ "location": { "$nearSphere": { "$geometry": 
    { "type": "Point", "coordinates": [ -73.93414657, 40.82302903 ] }, "$maxDistance": 5 * 1609.34 } } })
print(list(query3))