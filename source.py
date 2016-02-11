import sys
import json
import seaborn as sns

if len(sys.argv) != 2:
    print("You need to supply input filename")
    sys.exit(1)

fname = 'busy_day.in'
with open(fname, 'r') as inputfile:
    rows, cols, drones, turns, maxweight = [int(x) 
            for x in inputfile.readline().split()]
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

    item_type = 0

    colormap = [[0 for i in range(0, cols)] for j in range(0, rows)]
    for order in orders:
        itemcount = order[2][item_type]
        colormap[order[0][0]][order[0][1]] += itemcount


    sns.heatmap(colormap, annot=True, fmt="d")

