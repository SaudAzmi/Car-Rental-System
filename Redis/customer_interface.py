import math
import random
import time
import requests
import overpy
import redis
import pymongo


# Fetching all the customer data that are searching for a vehicle
def fetch_customer_data(cluster_name, collection_name):
    client = pymongo.MongoClient(
        "mongodb+srv://gk9713:DvZXo0a2WbphLM1r@cluster0.jufutvi.mongodb.net/?retryWrites=true&w"
        "=majority")

    db = client[cluster_name]
    collection = db[collection_name]

    customer_data = [tuple(data.values()) for data in collection.find({"searching": 1})]

    return customer_data


# fetch driver data that are available to drive
def fetch_driver_data(cluster_name, collection_name):
    client = pymongo.MongoClient(
        "mongodb+srv://gk9713:DvZXo0a2WbphLM1r@cluster0.jufutvi.mongodb.net/?retryWrites=true&w"
        "=majority")

    db = client[cluster_name]
    collection = db[collection_name]

    driver_data = [tuple(data.values())[:3] for data in collection.find({"available": 1})]

    return driver_data


# print(len(customers),customers[:2])
# print(type(customers[1]))

# Fetching data for all available car
def fetch_available_cars(cluster_name, collection_name):
    client = pymongo.MongoClient(
        "mongodb+srv://gk9713:DvZXo0a2WbphLM1r@cluster0.jufutvi.mongodb.net/?retryWrites=true&w"
        "=majority")

    db = client[cluster_name]
    collection = db[collection_name]

    available_cars = [tuple(data.values())[1:4] for data in collection.find({"available": 1})]

    return available_cars


# print(len(car_pick_ups), car_pick_ups[:2])

# Fetching data for available drop off locations
def fetch_drop_off_locations(cluster_name, collection_name):
    client = pymongo.MongoClient(
        "mongodb+srv://gk9713:DvZXo0a2WbphLM1r@cluster0.jufutvi.mongodb.net/?retryWrites=true&w"
        "=majority")

    db = client[cluster_name]
    collection = db[collection_name]

    drop_locations = [tuple(data.values())[1:4] for data in collection.find()]

    return drop_locations


# print(len(drop_off_locations), drop_off_locations)

# Ingestion function for redis


def redis_insertion(name, insert_data):
    for data in insert_data:
        r.geoadd(name, [data[2], data[1], data[0]])
    print(f"Successfully Ingested in {name}")


def check_car_availability(vehicle_distances):
    is_vehicle = []
    is_person = []
    for distance in vehicle_distances:
        vehicle = distance[0].decode()
        if vehicle.isdigit():
            is_person.append(distance)
        else:
            is_vehicle.append(distance)

    pick_up_locs = {}
    for vehicle in is_vehicle:
        pick_up_locs[vehicle[0].decode()] = vehicle[1]

    pick_up_locations_sorted = dict(sorted(pick_up_locs.items(), key=lambda x: x[1]))
    print(f"Near by Vehichle Pick-Up Locations are: {pick_up_locations_sorted} \n")

    nearest_pick_up_loc = [(k, v) for k, v in pick_up_locations_sorted.items()]
    print(f"Nearest Pick-Up Location: {nearest_pick_up_loc[0][0]} \n"
          f"Distance to nearest vehichle :{nearest_pick_up_loc[0][1]}")

    return pick_up_locs, nearest_pick_up_loc[0][0], nearest_pick_up_loc[0][1]


def vehicle_type():
    car_choice = str(input("The following are the car types available: \n"
                           "SUV       (Base Rate: Eur 35     Per Km: Eur 1.2)  \n"
                           "HATCHBACK (Base Rate: Eur 25     Per Km: Eur 0.8) \n"
                           "SEDAN     (Base Rate: Eur 30     Per Km: Eur 1)   \n"
                           "Please enter your choice: ")).upper()
    if car_choice not in ["SUV", "HATCHBACK", "SEDAN"]:
        print("You made an invalid choice, please try again! \n")
        vehicle_type()
    else:
        client = pymongo.MongoClient(
            "mongodb+srv://gk9713:DvZXo0a2WbphLM1r@cluster0.jufutvi.mongodb.net/?retryWrites=true&w"
            "=majority")

        db = client["LocationData"]
        collection = db["PickUpLocations"]

        available_cars = [tuple(data.values())[1:4] for data in collection.find({"available": 1,
                                                                                 "type": car_choice})]
        return available_cars, car_choice


def check_driver_availability(driver_distances):
    is_vehicle = []  # vehicle
    is_driver = []  # person
    for distance in driver_distances:
        vehicle = distance[0].decode()
        if vehicle.isdigit():
            is_driver.append(distance)
        else:
            is_vehicle.append(distance)

    driver_locs = {}
    for driver in is_driver:
        driver_locs[driver[0].decode()] = driver[1]

    driver_locations_sorted = dict(sorted(driver_locs.items(), key=lambda x: x[1]))
    print(f"Near by Driver by distance are: {list(driver_locations_sorted.items())[:10]} \n")

    nearest_driver_loc = [(k, v) for k, v in driver_locations_sorted.items()]
    print(f"Nearest Driver : {nearest_driver_loc[0][0]} \n")
    # f"Distance to selected vehichle :{nearest_driver_loc[0][1]} \n")

    return driver_locs, nearest_driver_loc[0][0]


def driver_rating():
    driver_rating_choice = int(input("The following are the driver rating types available: \n"
                                     "1. Between 1 and 3 stars (Base Rate: Eur 7     Per Km: Eur 0.5)  \n"
                                     "2. Between 3 and 4 stars (Base Rate: Eur 9     Per Km: Eur 0.7) \n"
                                     "3. Above 4 stars         (Base Rate: Eur 11     Per Km: Eur 1)   \n"
                                     "Please enter your choice: "))
    if driver_rating_choice not in [1, 2, 3]:
        print("You made an invalid choice, please try again! \n")
        driver_rating()
    else:
        min = 0
        max = 0
        if driver_rating_choice == 1:
            min = 1
            max = 3
        elif driver_rating_choice == 2:
            min = 3
            max = 4
        else:
            min = 4
            max = 5
        client = pymongo.MongoClient(
            "mongodb+srv://gk9713:DvZXo0a2WbphLM1r@cluster0.jufutvi.mongodb.net/?retryWrites=true&w"
            "=majority")

        db = client["LocationData"]
        collection = db["DriverLocation"]

        driver_data = [tuple(data.values())[:3] for data in
                       collection.find({"$and": [{"rating": {"$gte": min}}, {"rating": {"$lt": max}}]})]

        return driver_data, driver_rating_choice


def generateOTP():
    digits = [i for i in range(10)]
    otp_str = ""

    # creating a 6 digit long otp string
    for i in range(6):
        index = math.floor(random.random() * 10)
        otp_str += str(digits[index])

    # storing customer OTP in redis
    r.set("OTP_Customer", str(otp_str))
    r.expire("OTP_Customer", 20)

    print(f"Dear customer, please note your OTP for the service is: {otp_str} \n")

    # storing drive OTP in redis, will be same for driver or self driven
    r.set("OTP_Drive", str(otp_str))
    r.expire("OTP_Drive", 20)


def verifyOTP():
    otp_customer = r.get("OTP_Customer")
    otp_drive = r.get("OTP_Drive")

    otp_received = str(input("Dear customer please enter your OTP to start the trip: "
                             "\n"))

    # print(otp_customer.decode(), otp_drive.decode())

    if otp_received == str(otp_customer.decode()) and str(otp_customer == otp_drive.decode()):
        print("OTP verified successfully, enjoy your ride. \n")
    else:
        print("Invalid OTP, please try again! \n")
        verifyOTP()


def calc_time_mins(small_dist):
    # assuming that a person walks with an average speed of 5Km/Hr
    return round((small_dist / 5) * 60)


def calc_time_hrs(big_dist):
    # assuming that the speed of the car is 70Km/hr
    return round((big_dist / 70) * 60)


def display_distance_time(car_dist, drop_dist, driver_dist=None):
    if driver_dist is not None:
        print(f"The Chauffeur has begun his journey to pick up the vehicle. \n"
              f"He's at a distance of {driver_dist}Km. from the vehicle. \n"
              f"He will reach the vehicle in {calc_time_mins(driver_dist)} mins.\n")

        time.sleep(2)

        print(f"The Chauffeur has picked up the vehicle, he's on his way to take you to your destination. \n"
              f"Please be ready with the OTP to start the ride. \n"
              f"The vehicle is {car_dist}Km away. \n"
              f"It will reach your current position in {calc_time_mins(car_dist)} mins. \n")

        time.sleep(5)

        print(f"The Chauffeur has arrived at your location. \n"
              f"Your destination is {drop_dist}Km away. \n"
              f"You will reach your destination in {calc_time_hrs(drop_dist)} mins. \n")
        verifyOTP()

        time.sleep(10)

        print("Dear Customer, your ride has been completed. Thank you for using our service. \n")
        # Print ride completed message and display the total bill using the generate_invoice function

    else:
        print(f"Please be ready with the OTP to start the ride. \n"
              f"The vehicle is {car_dist}Km away. \n"
              f"You will reach the vehicle in {calc_time_mins(car_dist)} mins. \n")

        time.sleep(5)
        print(f"You have reached the vehicle. \n"
              f"Your destination is {drop_dist}Km away. \n"
              f"You will reach your destination in {calc_time_hrs(drop_dist)} mins. \n")
        verifyOTP()

        time.sleep(10)
        print("Dear Customer, your ride has been completed. \n")
        # Print ride completed message and display the total bill using the generate_invoice function


def cost_calculation(car_dist, drop_dist, driver_dist=None, car_type=None, rating_type=None):
    car_types = {"SUV": [35, 1.2], "HATCHBACK": [25, 0.8], "SEDAN": [30, 1]}
    rating_types = {"1": [7, 0.5], "2": [9, 0.7], "3": [11, 1]}
    total_dist = car_dist + drop_dist + driver_dist
    cost = 0
    if car_type == 1:
        cost += car_types[car_type][0] + total_dist * car_types[car_type][1]
    else:
        cost += 27 + total_dist * 0.9

    if rating_type is not None:
        cost += rating_types[str(rating_type)][0] + total_dist * rating_types[str(rating_type)][1]

    print(f"Dear customer, The total cost of the trip is Eur {cost}. \n"
          f"This amount will be directly debited from your account within 1 Day. Please ensure you have enough "
          f"balance in your account. \n"
          f"Thank you for using our services, hope to see you again soon! \n")


def store_ride_mongo(cluster_name, collection_name, data):
    client = pymongo.MongoClient(
        "mongodb+srv://gk9713:DvZXo0a2WbphLM1r@cluster0.jufutvi.mongodb.net/?retryWrites=true&w"
        "=majority")

    db = client[cluster_name]
    collection = db[collection_name]

    collection.insert_one(data)

    print("All ride details stored in Mongo successfully! End of session... \n")


def ride_confirmation(car_dist, drop_dist, driver_dist=None, car_type=None, rating_type=None):
    booking_confirmation = int(input("Are you happy with the choices and would like to confirm the booking? \n"
                                     "1. Yes   2. No \n"))
    if booking_confirmation == 1:
        print("Thank you for confirming the ride details! Your trip starts now. \n")
        generateOTP()
        display_distance_time(car_dist, drop_dist, driver_dist)
        cost_calculation(car_dist, drop_dist, driver_dist, car_type, rating_type)

    else:
        print("Ah, we apologise we couldn't be of your service again. Hope to see you soon! \n")


if __name__ == "__main__":
    cluster_name = "LocationData"
    collection_pickup = "PickUpLocations"
    collection_dropoff = "DropOffLocations"
    collection_customers = "CustomerLocations"
    collection_drivers = "DriverLocation"
    collection_ride = "Ride"

    # Creating the datasets to be ingested into redis
    customers = fetch_customer_data(cluster_name, collection_customers)
    drivers = fetch_driver_data(cluster_name, collection_drivers)
    car_pick_ups = fetch_available_cars(cluster_name, collection_pickup)
    drop_off_locations = fetch_drop_off_locations(cluster_name, collection_dropoff)

    r = redis.Redis(port=6379)  # Redis connection

    redis_insertion("drop_off", drop_off_locations)
    redis_insertion("customer", customers)

    # Creating the dataset to search in
    r.zunionstore("Temp", ("pick_up", "customer", "drop_off", "drivers"), aggregate="MIN")
    r.expire("Temp", 600)

    # Searching the nearest car for a random customer
    random_customer = customers[random.randrange(len(customers) - 1)]  # Generating a random customer
    print("Welcome to the Car Rental Interface \n\n")
    print(f"Hello Customer : {random_customer[0]} \n")
    # Display the details of the customer
    print(f"Your current latitude is: {random_customer[2]} \n "
          f"Your current longitude is: {random_customer[1]} \n\n")

    # Taking the user choice on type of vehicle
    vehicle_choice = int(input("Are you looking for a specific type of vehicle? \n"
                               "1. Yes    2. No \n"))
    type_of_car = None
    if vehicle_choice == 1:
        car_pick_ups, type_of_car = vehicle_type()
    else:
        print("We will be recommending the nearest vehicle to you to help you reach your destination"
              "as soon as possible! \n")

    redis_insertion("pick_up", car_pick_ups)

    # Taking in the choice of radius to check car availability
    radius = int(input("Please input the radius to search the available car in: \n"))

    vehicle_distances = r.georadiusbymember("Temp", random_customer[0], unit="km", withdist=True,
                                            radius=radius)  # withcoord=True

    pick_up_locations, nearest_pick_up_location, dist_nearest_pick_up_location = check_car_availability(
        vehicle_distances)

    # Generating a random drop off location
    drop_location = drop_off_locations[random.randrange(len(drop_off_locations) - 1)]
    print(f"Your drop location is: {drop_location[0]} \n "
          f"Drop latitude is : {drop_location[2]} \n "
          f"Drop longitude is : {drop_location[1]} \n")

    # Calculating the distance to drop off using redis
    distance_to_drop_off = r.geodist("Temp", nearest_pick_up_location, drop_location[0], unit="km")
    print(f"Distance between Pick-Up and Drop-Off: {distance_to_drop_off} Km \n")

    # Taking the users choice on a driver
    driver_choice = int(input("Would you like a Chauffeur for this ride? \n"

                              "1. Yes   2. No \n"))

    # Searching the nearby drivers to the vehicle
    driver_rating_range = None
    if driver_choice == 1:

        driver_rating_choice = int(input("Are you looking for a driver of particular rating? \n"
                                         "1. Yes    2. No \n"))

        if driver_rating_choice == 1:
            drivers, driver_rating_range = driver_rating()
        else:
            print("We will be recommending the nearest driver to your selected vehicle "
                  "to help you reach your destination"
                  "as soon as possible! \n\n")

        redis_insertion("drivers", drivers)

        r.zunionstore("TempDriver", ("pick_up", "drivers"), aggregate="MIN")
        r.expire("Temp", 600)
        driver_distances = r.georadiusbymember("TempDriver", nearest_pick_up_location, unit="km", withdist=True,
                                               radius=radius)
        # print(driver_distances)
        driver_locations, nearest_driver_location = check_driver_availability(driver_distances)

        # Calculating the distance from driver to vehicle using redis
        distance_from_driver_to_car = r.geodist("Temp", nearest_driver_location, nearest_pick_up_location, unit="km")
        print(f"Distance between Driver and Vehicle: {distance_from_driver_to_car} Km \n")

        ride_confirmation(car_dist=int(dist_nearest_pick_up_location), drop_dist=int(distance_to_drop_off),
                          driver_dist=int(distance_from_driver_to_car), car_type=type_of_car,
                          rating_type=driver_rating_range)

    else:
        print("Opted out for the Chauffeur Service \n")
        ride_confirmation(car_dist=int(dist_nearest_pick_up_location), drop_dist=int(distance_to_drop_off))

    data_for_mongo = {
        'customer_id': random_customer[0],
        'customer_lat': random_customer[2],
        'customer_long': random_customer[1],
        'car_type': type_of_car,
        'car_pickup_loc': nearest_pick_up_location,
        'drop_loc': drop_location[0],
        'drop_lat': drop_location[2],
        'drop_long': drop_location[1],
        'driver_choice': driver_choice,
        'driver_rating_range': driver_rating_range
    }

    store_ride_mongo(cluster_name=cluster_name, collection_name=collection_ride, data=data_for_mongo)
