# Sravani Yerramaneni 001359531

import datetime


class Truck:
    # Time complexity of O(1)
    def __init__(self, start_time, package_list, address_ids_dict):
        self.start_time = start_time              # the time the truck departs from the hub to deliver packages
        self.end_time = datetime.time(0, 0, 0)    # the time the truck returns to the hub after delivering all packages
        self.package_list = package_list          # contains all the packages to be delivered by the truck
        self.address_package_dict = address_ids_dict  # contains address_ids that map to their respective packages
        self.package_route = []                   # contains packages in the order they will be delivered
        self.distance = 0

    # end_time is set in the main.route() function after the routes are created
    # Time complexity of O(1)
    def set_end_time(self, end_time):
        self.end_time = end_time

    # package_route is set in the main.route() function after the routes are created
    # Time complexity of O(1)
    def set_package_route(self, package_route):
        self.package_route = package_route


class HashTable:
    # Time complexity of O(N) where N is the length of the hash_table list
    def __init__(self, capacity=41):
        self.capacity = capacity
        self.hash_table = [None] * capacity     # The list stores package information as lists
        self.indexes = []    # Keeps track of list indices that are populated with elements

    # Will always return inputted key because the length of hash_table will always be bigger than key
    # Time complexity of O(1)
    def hash(self, key):
        return key % len(self.hash_table)

    # Time complexity of O(k)
    def insert(self, id1, address, deadline, city, zip_code, weight, status="AT HUB", routed=False):
        index = id1
        address = address
        if address in address_dict.keys():  # uses the address_dict dictionary to map the address string to an integer
            address_id = address_dict.get(address)
        else:
            address_id = -1
        deadline = deadline
        city = city
        zip_code = zip_code
        weight = weight
        status = status
        routed = routed     # Used to distinguish packages created through the interface
        delivery_time = datetime.time(23, 59, 59)       # Will be set when the package is routed
        truck_start_time = datetime.time(23, 59, 59)    # Will be set when the package is routed

        if index > self.capacity:
            # Time complexity of O(k) where k is index-self.capacity+1
            self.hash_table.extend([None] * (index-self.capacity+1))

        key = self.hash(index)      # key will always equal the index
        self.hash_table[key] = [index,        # 0
                                address,      # 1
                                deadline,     # 2
                                city,         # 3
                                zip_code,     # 4
                                weight,       # 5
                                status,       # 6
                                address_id,   # 7
                                routed,       # 8
                                delivery_time,     # 9
                                truck_start_time]  # 10
        self.indexes.append(index)      # Keeps track of the indexes in use in order to avoid collisions

    # Time complexity of O(1)
    def get(self, package_id):
        return self.hash_table[package_id]

    # Return specific package information from package list
    # Time complexity of O(1)
    def search(self, package_id, string):
        p = self.hash_table[package_id]
        if string == "address":
            return p[1]
        if string == "deadline":
            return p[2]
        if string == "city":
            return p[3]
        if string == "zip_code":
            return p[4]
        if string == "weight":
            return p[5]
        if string == "status":
            return p[6]
        if string == "address_id":
            return p[7]
        if string == "routed":
            return p[8]
        if string == "delivery_time":
            return p[9]
        if string == "truck_start_time":
            return p[10]

    # truck_start_time is set in the main.pick_truck() function
    # Time complexity of O(1)
    def set_truck_start_time(self, index, start_time):
        self.hash_table[index][10] = start_time

    # delivery_time is set in the main.route() function when the route is created
    # Time complexity of O(1)
    def set_delivery_time(self, index, delivery_time):
        self.hash_table[index][9] = delivery_time

    # Used to modify package 9's address
    # Time complexity of O(1)
    def set_address(self, index, address):
        self.hash_table[index][1] = address
        if address in address_dict.keys():
            self.hash_table[index][7] = address_dict.get(address)

    # Used to modify package 9's address
    # Time complexity of O(1)
    def set_zip_code(self, index, zip_code):
        self.hash_table[index][4] = zip_code

    # Used to distinguish between packages that are routed and packages that aren't
    # Only packages created through the interface are not routed
    # Time complexity of O(1)
    def set_routed(self, index, routed):
        self.hash_table[index][8] = routed

    # Time complexity of O(1)
    def set_status(self, index, status):
        self.hash_table[index][6] = status

    # Time complexity of O(1)
    def print(self, package_id, time):
        address = self.search(package_id, "address") + ", " + \
                  self.search(package_id, "city") + " " + \
                  str(self.search(package_id, "zip_code"))

        deadline = self.search(package_id, "deadline")
        if deadline == datetime.time(23, 59, 59):
            deadline = "EOD"
        else:
            deadline = str(deadline)  # Converts deadline to a string so it's easier to format when printing

        # Packages created through the user interface are not routed
        # If a package is not routed, then it's status should stay the same
        # since its truck_start_time and delivery_time are set to default values
        if self.search(package_id, "routed"):
            status = "AT HUB"
            if self.search(package_id, "truck_start_time") <= time:
                status = "EN ROUTE"
            if self.search(package_id, "delivery_time") < time:
                status = "DELIVERED"
        else:
            status = self.search(package_id, "status")
        self.set_status(package_id, status)

        print("{} \t"
              "{:^60s}\t"
              "Deadline: {:<15s}"
              "Weight: {:<10d} \t"
              "Status: {} \t".format(package_id, address, deadline, self.search(package_id, "weight"), status))

    # Iterates over and prints all package information
    # Time complexity of O(N) where N is the number of total packages
    def print_all(self, time):
        for i in self.indexes:
            self.print(i, time)


# Maps address (str) -> address_id (int)
# Populated in main.load_data()
address_dict = {}
