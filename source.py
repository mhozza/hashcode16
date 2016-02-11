#!/usr/bin/env python3
import sys
import math
# import seaborn as sns

if len(sys.argv) != 2:
    print("You need to supply input filename")
    sys.exit(1)

fname = 'busy_day.in'
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

def dist(s, t):
    '''Computes euclidian distance between source and target position'''
    return math.ceil(math.sqrt((s[0]-t[0])**2 + (s[1]-t[1])**2))


def item_from_closest_warehouse(item, target_position):
    '''returns closest warehouse and it's dist from the item target'''
    closest = (float('inf'), None)  #dist, warehouse
    for i, warehouse in enumerate(warehouses):
        if warehouse[1][item]:
            if closest[0] > dist(target_position, warehouse[0]):
                closest = dist(target_position, warehouse[0]), i
    return closest


def select_min_order():
    minimal = (float('inf'), None)
    for i, (order_position, _, items) in enumerate(orders):
        order_duration = max(
            item_from_closest_warehouse(item, order_position)[0] for item in items
        )
        if order_duration < minimal[0]:
            minimal = (order_duration, i)
    return minimal

print(select_min_order())

total_score = 0
def deliver_order(turn):
    # Computes score
    score = math.ceil((turns - turn)/turns * 100)
    total_score += score


print("Total score {}".format(total_score))