#prompts user for order from menu and displays total cost
import sys

menu = {
    "Baja Taco": 4.00,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
}

total_cost = 0
while True:
    try:
        item = input("Item: ")
        item = item.title()
        if item in menu:
            total_cost += menu[item]
            print("Total: $" + "%.2f" % total_cost)
    except EOFError:
        print()
        sys.exit(0)

