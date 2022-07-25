#https://towardsdatascience.com/driving-distance-between-two-or-more-places-in-python-89779d691def


import requests
import json
from geopy.geocoders import Nominatim
from geopy import distance
from numpy import place

geolocator=Nominatim(user_agent="geoapiExercises")

#place input
input_place1="Mannheim"
input_place2="Stuttgart"

#location of the place
place1=geolocator.geocode(input_place1)
place2=geolocator.geocode(input_place2)

#Get Latitude and Longitude

loc1_lat,loc1_long=(place1.latitude),(place1.longitude)
loc2_lat,loc2_long=(place2.latitude),(place2.longitude)

# call the OSMR API
long1,latt1=8.6820917,50.1106444 #frankfurt


#mannheim to heidelberg
r = requests.get(f"http://router.project-osrm.org/route/v1/car/{loc1_long},{loc1_lat};{loc2_long},{loc2_lat}?overview=false""")
# then you load the response using the json libray
# by default you get only one alternative so you access 0-th element of the `routes`
routes = json.loads(r.content)
# route_1 = routes.get("routes")[0]
route_1 = routes.get("routes")[0]
# print(route_1)

print("Distance betweeen ", input_place1,input_place2)
print(route_1.get("distance")/1000," km")






point1=routes.get("waypoints")



# print("--------")
# print(point1)


#Get the intermediate points
# for i in point1:
#     print(i['name'],i['distance'],i['location'])


