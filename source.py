#!/usr/bin/env python3
import sys
import math
from collections import defaultdict

if len(sys.argv) != 2:
    print("You need to supply input filename")
    sys.exit(1)

fname = sys.argv[1]
with open(fname, 'r') as inputfile:
    rows, cols, drones, turns, maxweight = [
        int(x)
        for x in inputfile.readline().split()
    ]
    product_count = int(inputfile.readline())
    products = [int(x) for x in inputfile.readline().split()]

    warehouse_count = int(inputfile.readline())
    warehouses = [(
        tuple(int(x) for x in inputfile.readline().split()),
        [int(x) for x in inputfile.readline().split()]
    ) for i in range(0, warehouse_count)]

    # Warehouse is a tuple (position, list of item counts (per item id))

    orders_count = int(inputfile.readline())
    orders = [(
        tuple(int(x) for x in inputfile.readline().split()),
        int(inputfile.readline()),
        [int(x) for x in inputfile.readline().split()]
    ) for i in range(0, orders_count)]

    # Order is a tuple (position, count of items, list of item ids)

completed_orders = {}
completed_items_per_order = [set() for i in range(len(orders))]
num_completed_orders = 0


def order_completed(order):
    return order in completed_orders


def item_completed(order, item_index):
    return item_index in completed_items_per_order[order]

commands = []

def dist(s, t):
    '''Computes euclidian distance between source and target position'''
    return math.ceil(math.sqrt((s[0]-t[0])**2 + (s[1]-t[1])**2))


def item_from_closest_warehouse(item, target_position):
    '''returns closest warehouse and it's dist from the item target'''
    closest = (float('inf'), None)  # dist, warehouse
    for i, warehouse in enumerate(warehouses):
        if warehouse[1][item]:
            if closest[0] > dist(target_position, warehouse[0]):
                closest = dist(target_position, warehouse[0]), i
    return closest


def select_min_order():
    minimal = (float('inf'), None)
    for order_index, (order_position, _, items) in filter(lambda x: not order_completed(x[0]), enumerate(orders)):
        item_durations = [item_from_closest_warehouse(item, order_position)[0] for item in items]
        order_duration = max(item_durations) if len(item_durations) else float('inf')
        if order_duration < minimal[0]:
            minimal = (order_duration, order_index)
    return minimal


total_score = 0
def deliver_order(turn):
    # Computes score
    score = math.ceil((turns - turn)/turns * 100)
    global total_score
    total_score += score

class DroneManager:
    # Drone positions when its current task is finished
    # Drones start at first warehouse
    drone_positions = [(warehouses[0][0]) for i in range(0, drones)]

    # When will be drone available
    drone_availability = [0 for i in range(0, drones)]

    def find_fastest_available_drone(self, x, y):
        drone_times = [self.drone_availability[k] + dist(self.drone_positions[k], (x, y)) + 1 for k in range(0, drones)]

        return drone_times.index(min(drone_times))

    def allocate_drone(self, itemcounts, w, order):
        warehouse = warehouses[w]
        drone = self.find_fastest_available_drone(*warehouse[0])
        for i, count in itemcounts:
            commands.append('{} L {} {} {}'.format(drone, w, i, count))

        for i, count in itemcounts:
            commands.append('{} D {} {} {}'.format(drone, order, i, count))
        target = orders[order][0]

        total_time = self.drone_availability[drone] + dist(self.drone_positions[drone], warehouse[0]) + 1 + dist(warehouse[0], target) + 1
        self.drone_availability[drone] = total_time
        self.drone_positions[drone] = target

        return total_time

    def deal_with_order(self, order):
        # For each item in order, allocate a drone to it
        target = orders[order][0]
        item_times = []

        warehouse_items_counts = defaultdict(lambda: defaultdict(int))

        for i in orders[order][2]:
            closest = item_from_closest_warehouse(i, target)[1]
            warehouse_items_counts[closest][i] += 1

        deliveries = []
        for w in warehouse_items_counts:
            ware = warehouse_items_counts[w]
            def is_something_in_warehouse(ware):
                for k in ware:
                    if ware[k] != 0:
                        return True
                return False

            while is_something_in_warehouse(ware):
                items = []
                current_weight = 0
                for i in ware:
                    available_weight = maxweight - current_weight
                    item_weight = products[i]
                    available_count = available_weight // item_weight
                    available_count = min(available_count, ware[i])
                    if (available_count == 0):
                        continue
                    set_weight = item_weight * available_count
                    current_weight += set_weight
                    items.append((i, available_count))
                    ware[i] -= available_count
                    warehouses[w][1][i] -= available_count

                res = self.allocate_drone(items, w, order)
                item_times.append(res)                

        end_time = max(item_times)

        completed_orders[order] = end_time
        deliver_order(end_time)
        global num_completed_orders
        num_completed_orders += 1

        return end_time


dm = DroneManager()
print("Total orders {}".format(orders_count))

while num_completed_orders != orders_count:
    if num_completed_orders % 10 == 0:
        print(num_completed_orders)
    end_time = dm.deal_with_order(select_min_order()[1])
    if end_time > turns:
        break


outfname = 'output.txt'
with open(outfname, 'w+') as outfile:
    outfile.write(str(len(commands)))
    outfile.write('\n')
    for line in commands:
        outfile.write(line)
        outfile.write('\n')

print("Total score {}".format(total_score))
