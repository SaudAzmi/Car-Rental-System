import json
import requests
import overpy
import pymongo
import random
import numpy

api = overpy.Overpass()  # Overpass API

# Query to get geospatial data from OpenStreetMap

request = api.query("""
area["ISO3166-2"="FR-74"][admin_level=6];
(
  node[place~"^(city|town|village)$"](area);
);
out center;
""")

# We only take city name, longitude and latitude
cities = []
cities += [(node.tags["name"], float(node.lon), float(node.lat)) for node in request.nodes]

# print(len(cities))
# print(type(cities))
# print(cities[:10])

pick_ups = cities[:160]
drop_offs = cities[160:]

customer_request = api.query("""
area["ISO3166-2"="FR-74"][admin_level=6];
(
  node["amenity"="restaurant"](area);
);
out center;
""")

# print(request.nodes)

# We only take city name, longitude and latitude
customers = []
customers += [(str(node.id), float(node.lon), float(node.lat)) for node in customer_request.nodes]

# print(pick_ups[:5])
# print(drop_offs[:5])


driver_request = api.query("""
area["ISO3166-2"="FR-74"][admin_level=6];
(
  node["amenity"="cafe"](area);
);
out center;
""")

drivers = []
drivers += [(str(node.id), float(node.lon), float(node.lat)) for node in driver_request.nodes]


def create_pickup_location_data(locations):
    insert_data_list = []
    for i in range(len(locations)):
        insert_data_list.append({
            "_id": i,
            "location_name": locations[i][0],
            "lon": locations[i][1],
            "lat": locations[i][2],
            "type": str(random.choice(["SUV", "SEDAN", "HATCHBACK"])),
            "available": int(numpy.random.choice([0, 1]))
        })
    return insert_data_list


def create_drop_location_data(locations):
    insert_data_list = []
    for i in range(len(locations)):
        insert_data_list.append({
            "_id": i,
            "location_name": locations[i][0],
            "lon": locations[i][1],
            "lat": locations[i][2]
        })
    return insert_data_list


def create_customer_location_data(locations):
    insert_data_list = []
    for i in range(len(locations)):
        insert_data_list.append({
            "_id": locations[i][0],
            "lon": locations[i][1],
            "lat": locations[i][2],
            "searching": int(numpy.random.choice([0, 1]))
        })
    return insert_data_list


def create_driver_location_data(locations):
    insert_data_list = []
    for i in range(len(locations)):
        insert_data_list.append({
            "_id": locations[i][0],
            "lon": locations[i][1],
            "lat": locations[i][2],
            "available": int(numpy.random.choice([0, 1])),
            "rating": round(random.uniform(1, 5), 1)
        })
    return insert_data_list


def insert_to_mongo(cluster_name, collection_name, insert_data):
    client = pymongo.MongoClient(
        "mongodb+srv://gk9713:DvZXo0a2WbphLM1r@cluster0.jufutvi.mongodb.net/?retryWrites=true&w"
        "=majority")

    db = client[cluster_name]
    collection = db[collection_name]

    collection.delete_many({})
    print(f"Emptied the collection {collection_name}")

    for data in insert_data:
        collection.insert_one(data)

    print(f"{len(insert_data)} data points inserted successfully in collection {collection_name}!")


insert_pick_up_data = create_pickup_location_data(pick_ups)
insert_drop_off_data = create_drop_location_data(drop_offs)
insert_customer_location_data = create_customer_location_data(customers)
insert_driver_location_data = create_driver_location_data(drivers)

"""print(len(insert_pick_up_data), insert_pick_up_data[:2])
print(len(insert_drop_off_data), insert_drop_off_data[:2])
print(len(insert_customer_location_data), insert_customer_location_data[:2])
print(len(insert_driver_location_data), insert_driver_location_data[:2])
"""
cluster_name = "LocationData"
collection_pickup = "PickUpLocations"
collection_dropoff = "DropOffLocations"
collection_customers = "CustomerLocations"
collection_drivers = "DriverLocation"

insert_to_mongo(cluster_name, collection_pickup, insert_pick_up_data)
insert_to_mongo(cluster_name, collection_dropoff, insert_drop_off_data)
insert_to_mongo(cluster_name, collection_customers, insert_customer_location_data)
insert_to_mongo(cluster_name, collection_drivers, insert_driver_location_data)

