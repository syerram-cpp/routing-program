# Sravani Yerramaneni 001359531

import csv
import datetime

# Creates hash table with all package data
# Creates dictionary that maps address to an integer
from objects import HashTable, Truck
from objects import address_dict


def load_data():
    # The function load_data() has a Time Complexity of O(N^2).

    global package_hash  # HashTable that contains an array of packages with indexes being the packages' ids
    global distances_list   # Adjacency list that contains the distances between all addresses

    # Time complexity is O(N)
    with open('address.csv') as f:  # Populates dictionary that maps addresses to an address ID integer
        csv_file = csv.DictReader(f, delimiter=',')
        for row in csv_file:
            address_dict[row["Address"]] = int(row["Address ID"])

    # Time complexity is O(N)
    with open('package.csv') as f:  # Inserts all package information into hash-table
        csv_file = csv.DictReader(f, delimiter=',')
        for row in csv_file:
            if row["Delivery Deadline"] == "EOD":
                deadline = datetime.time(23, 59, 59)
            else:
                deadline_str = row["Delivery Deadline"]
                deadline = datetime.time(int(deadline_str[0:2]), int(deadline_str[3:5]), 00)
            package_hash.insert(int(row["Package ID"]),
                                row["Address"],
                                deadline,
                                row["City"],
                                int(row["Zip"]),
                                int(row["Mass"]))

    address_id = 0
    # Time complexity of O(N^2)
    for line in open("distance.csv"):   # Populates distances_list
        csv_row = line.split('\n')
        distances_list.append([])  # Initializes list at index=address_id before appending to it

        for distance in csv_row[0].split(", "):     # Appends each distance to the address_id's list of distances
            distances_list[address_id].append((float(distance)))
        address_id = address_id + 1


def pick_truck():
    # Three trucks represent 3 loads of packages and/or 3 round-trips
    global truck1
    global truck2
    global truck3

    # Start times are chosen to be the 3 different times that packages are available by:
    truck1_start_time = datetime.time(8, 0, 0)
    truck2_start_time = datetime.time(9, 5, 0)      # Packages 6, 25, 28, and 32 don't arrive to the hub until 9:05 AM
    truck3_start_time = datetime.time(10, 20, 0)    # Package 9's address is not available until 10:20 AM

    # List of packages to be delivered by the truck, unordered
    truck1_packages = []
    truck2_packages = []
    truck3_packages = []

    # Dictionary that maps address_ids to their corresponding packages
    # Accounts for multiple packages delivering to the same address
    # by only counting that address once
    truck1_addresses = {}
    truck2_addresses = {}
    truck3_addresses = {}

    # List of package IDs manually assigned to each truck
    truck1_ids = [14, 15, 16, 34, 20, 21, 3, 8, 30, 5, 37, 38, 13, 39, 7, 29]
    truck2_ids = [25, 26, 4, 40, 1, 28, 2, 33, 6, 31, 32, 12, 17, 36, 19]

    # Iterates through all packages and assigns each package to a truck according to the lists above
    # Populates each truck's address-package dictionary
    # Time complexity is O(N) where N is equal to the number of total packages
    for i in package_hash.indexes:   # i is the package id
        address_id = package_hash.search(i, "address_id")
        if i in truck1_ids:
            truck1_packages.append(i)
            # Checks if the package's address id already exists in the dictionary to avoid overwriting a key
            if address_id in truck1_addresses.keys():
                truck1_addresses[address_id].append(i)
            else:
                truck1_addresses[address_id] = [i]
        elif i in truck2_ids:
            truck2_packages.append(i)
            if address_id in truck2_addresses.keys():
                truck2_addresses[address_id].append(i)
            else:
                truck2_addresses[address_id] = [i]
        else:   # if the package's id is not in truck1's or truck2's list of ids, the package is assigned to truck3
            truck3_packages.append(i)
            if address_id in truck3_addresses.keys():
                truck3_addresses[address_id].append(i)
            else:
                truck3_addresses[address_id] = [i]

    # Creates the 3 trucks initializing their start times, packages list, and address dictionary
    # Time complexity of O(1)
    truck1 = Truck(truck1_start_time, truck1_packages, truck1_addresses)
    truck2 = Truck(truck2_start_time, truck2_packages, truck2_addresses)
    truck3 = Truck(truck3_start_time, truck3_packages, truck3_addresses)


def route(truck):
    global mileage
    global delivered_by_deadline    # Boolean that checks whether all packages comply with their delivery deadlines

    address_package_dict = truck.address_package_dict       # Maps each address ID to a list of packages

    package_route = []  # Used to store the package IDs in the order in which they will be delivered
    addresses_to_route = list(address_package_dict.keys())  # Stores the addresses on the truck's route

    clock = datetime.datetime.combine(date, truck.start_time)     # Used to set delivery_time for each package
    total_distance = 0
    curr_address = 0    # Initialized to 0 to find the address closest to the hub (address ID of hub is 0)

    # Asymptotic Time complexity of O(N^2)
    for i in range(len(truck.address_package_dict)+1):
        if i == len(truck.address_package_dict):    # Used to map the last address back to the hub
            addresses_to_route.append(0)

        # Next address is computed through the find_next_address() function
        next_address_info = find_next_address(curr_address, addresses_to_route)
        curr_address = next_address_info[0]     # curr_address is assigned to next address
        distance = next_address_info[1]

        addresses_to_route.remove(curr_address)     # Time Complexity of O(N)

        # Distance and time of above trip are added to total distance and total time
        total_distance = total_distance + distance
        minutes = (distance / speed) * 60
        clock = clock + datetime.timedelta(minutes=minutes)

        if curr_address != 0:   # address 0 is not in the address_package_dict
            p_list = address_package_dict.get(curr_address)  # Returns list of packages that deliver to prev_address_id
            # Time complexity of O(N)
            # Adds each package that delivers to curr_address to the package_route
            for id in p_list:
                package_hash.set_truck_start_time(id, truck.start_time)
                package_hash.set_delivery_time(id, clock.time())
                package_hash.set_routed(id, True)
                package_route.append(id)

                delivery_time = package_hash.search(id, "delivery_time")
                deadline = package_hash.search(id, "deadline")
                if delivery_time > deadline:    # Checks if each package is delivered by its delivery deadline
                    delivered_by_deadline = False

    # Time complexity of O(1)
    truck.distance = total_distance
    truck.set_package_route(package_route)
    truck.set_end_time(clock.time())

    mileage = mileage + truck.distance


def find_next_address(curr_address, addresses_to_route):
    min_distance = -1
    next_address = -1

    # Starting from the curr_address, finds the next closest address from the addresses_to_route list
    # Time Complexity of O(N)
    for address in addresses_to_route:
        distance = distances_list[curr_address][address]
        if distance < min_distance or min_distance == -1:
            min_distance = distance
            next_address = address
    return [next_address, min_distance]


def check_status():
    # Time Complexity may not apply to the check_status() function
    # because the loop is meant to run until the user decides to exit it.
    # Also, inside the main while loop, there are nested while loops that keep
    # prompting the user for input until a valid input is inputted.

    print("Enter 'exit' to exit at any time except when inserting a package.\n")
    while True:     # Returns when string 'exit' is inputted
        insert_str = input("Enter 'insert' to insert a package.\n"
                           "To look-up package information, enter 'l': ")
        if insert_str == 'exit':
            return
        print()
        if insert_str == 'insert':
            insert_package()
            print()
            continue

        time = get_valid_time()
        if time == 'exit':
            return

        # Sets address of package #9 based on the time
        if time < datetime.time(10, 20, 00):
            package_hash.set_address(9, "300 State St")
            package_hash.set_zip_code(9, 84103)
        else:
            package_hash.set_address(9, "410 S State St")
            package_hash.set_zip_code(9, 84111)

        package_no = get_valid_package_no()
        if package_no == 'exit':
            return

        print()
        # Prints the package information based on the user's input
        if package_no == "all":
            package_hash.print_all(time)    # Time complexity of O(N) where N is the number of packages
        else:
            package_hash.print(package_no, time)


def get_valid_time():
    # Time complexity may not apply to the get_valid_time() function
    # because the loop is meant to run until the user inputs
    # a valid value. So time complexity would be O(infinity)
    while True:
        try:
            time = input("[EXAMPLE: 13:30] Enter a time in 24-hour format: ")
            if time == 'exit':
                return time
            if len(time) < 5:   # Used to convert '9:30' into '09:30'
                time = "0" + time
            time = datetime.time(int(time[:2]), int(time[3:5]))
            return time
        except ValueError:
            print("Enter a valid time.")
            continue


def get_valid_package_no():
    # Checks for a valid package number
    # Time complexity may not apply to the get_valid_package_no() function
    # because the loop is meant to run until the user inputs
    # a valid value. So time complexity would be O(infinity)

    package_input = input("[Enter 'all' for all packages.] Enter a package number: ")
    while True:     # Returns when a valid package value is inputted: either 'exit', 'all', or an integer
        if package_input == "all" or package_input == 'exit':
            return package_input
        try:
            package_no = int(package_input)
            # Valid values are any positive integer that is not already being used as a package's id
            if package_no not in package_hash.indexes:   # Checks if the package exists
                print("Enter 'all' or a valid package number.")
                package_input = input("[Enter 'all' for all packages.] Enter a package number: ")
            else:
                return package_no
        except ValueError:
            print("Enter 'all' or a valid package number.")
            package_input = input("[Enter 'all' for all packages.] Enter a package number: ")


def insert_package():
    # Time complexity may not apply to the get_valid_time() function
    # because the while loop is meant to run until the user inputs
    # a valid value for the id. So time complexity would be O(infinity)
    try:
        print("There is no option to exit the program while inserting a package.")
        input_id = input("Enter package ID: ")

        # Checks if package id already exists or is a negative integer
        while int(input_id) in package_hash.indexes or int(input_id) < 0:
            print("That package ID already exists. Please enter another one.")
            input_id = input("Enter package ID: ")
        address = input("Enter address: ")
        deadline = input("Enter deadline in 24-hour format [e.g. 13:30] or enter 'EOD' for end of day: ")
        if deadline == "EOD" or deadline == "eod":
            deadline = datetime.time(23, 59, 59)
        else:
            if len(deadline) < 5:
                deadline = "0" + deadline
            deadline = datetime.time(int(deadline[0:2]), int(deadline[3:5]), 00)
        city = input("Enter city: ")
        zip_code = int(input("Enter zip code: "))
        weight = int(input("Enter weight: "))
        status = input("Enter status: ")
        package_hash.insert(int(input_id), address, deadline, city, zip_code, weight, status)
        print("\nPackage inserted successfully.\n")
    except ValueError:    # Either time, zip_code, or weight was inputted wrong
        print("Enter valid package information.")


date = datetime.date(2020, 9, 4)    # Used to convert time values into datetime when a timedelta needs to be used
speed = 18                          # Speed of truck
mileage = 0     # Total mileage on the trucks; Each truck's distance is added to it in the route() function
delivered_by_deadline = True    # Set to false in route() if a package's delivery time is after its deadline

package_hash = HashTable()   # Hash-table that contains a list of all packages
distances_list = []  # Adjacency list that stores a list of distances for each address

load_data()  # Fills the package_hash, distances_list, and address_dict with data from .csv files

# Fixes the wrong address of package #9
package_hash.set_address(9, "410 S State St")
package_hash.set_zip_code(9, 84111)

truck1, truck2, truck3 = None, None, None
pick_truck()  # Assigns the manually created package lists to each truck

# Decides the route for the packages on each truck
route(truck1)
route(truck2)
route(truck3)

print("\nTOTAL MILEAGE:", mileage)
if delivered_by_deadline:
    print("ALL PACKAGES DELIVERED ON TIME.\n")

check_status()
