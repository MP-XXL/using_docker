# Online Store Inventory & Sales System
store = {
        "Laptop":{"price": 1200, "quantity": 5},
        "Headphones": {"price": 150, "quantity": 10},
        "Mouse": {"price": 40, "quantity": 20}
        }
def start():
    while True:
        option = int(input("""
                WELCOME TO THE IVENTORY

                1. Enter \"1\" to add product to iventory.
                2. Enter \"2\" to update stock in inventory.
                3. Enter \"3\" to initiate sale for a product.
                4. Enter \"4\" to view current inventory.
                5. Enter \"5\" to view most expensive product in the inventory
                6. Enter \"6\" to view the total value of all remaining stock
                7. Enter \"0\" to exit the inventory
                \n>>> : """))
        if option == 0:
            print("Program terminated!")
            break
        user_choice(option)
def user_choice(choice_option):
    if choice_option == 1:
        product = input("Enter product name to add to inventory: ").capitalize()
        price = int(input("Enter product price : "))
        quantity = int(input("Enter product quantity: "))
        add_product(store, product, price, quantity)
    elif choice_option == 2:
        product = input("Enter name of product to update: ").capitalize()
        new_quantity = int(input("Enter the quantity to add or reduce : "))
        update_stock(store, product, new_quantity)
    elif choice_option == 3:
        product = input("Enter product name you want to sell : ").capitalize()
        quantity_to_sell = int(input("Enter the quantity to sell : "))
        sell_product(store, product, quantity_to_sell)
    elif choice_option == 4:
        display_inventory(store)
    elif choice_option == 5:
        most_expensive_product(store)
    elif choice_option == 6:
        total_value = total_potential_sales(store)
        print(f"The current inventory is valued at {total_value :,.2f}")
    else:
        print("Invalid command!")
# Adding a new product to the to inventory
def add_product(store, name, price, quantity):
    if name in store:
        print("Product already exists in the inventory. Use the update inventory option")
    else:
        store[name] = {"price": price, "quantity": quantity}
        print(f"Product added successfully! Product details = Name: {name}, Price: {store[name]['price']}, Quantity: {store[name]['quantity']}")
# Updating stock
def update_stock(store, name, quantity):
    if name not in store:
        print("Prouct not found! Try the add product option.")
    else:
        while True:
            update_math = int(input("Enter \"1\" to add to stock or \"2\" to reduce from stock : "))
            if update_math == 1:
                store[name]["quantity"] += quantity
                print(f"Item updated successfully! {quantity} {store[name]} have been added to stock!")
                print("UPDATED INVENTORY")
                for item in store:
                    print(f"Name = {item}: Price:{store[item]['price']}, Quantity:{store[item]['quantity']}")
                break
            elif update_math == 2:
                if quantity > store[name]["quantity"]:
                    print("Inputed quantity to reduce greater than available quantity. Please view total iventory for accurate stock value.")
                else:
                    store[name]["quantity"] -= quantity
                    print(f"Item update successfully! {quantity} {store[name]} have been removed from stock!")
                    print("UPDATED INVENTORY")
                    for item in store:
                        print(f"Name = {item}: Price:{store[item]['price']}, Quantity:{store[item]['quantity']}")

                    break
            else:
                print("Invalid command!")
# Selling a product
def sell_product(store, name, quantity):
    if name not in store:
        print("Item is out of stock!")
    else:
        if quantity > store[name]["quantity"]:
            print("Insufficient product quantity. Desired quantity to sell is greater than available quantity. Please view total inventory for accurate stock value.")
        else:
            store[name]["quantity"] -= quantity
            print("Sale successful!")
            total_sale = quantity * store[name]["price"]
            print(f"A quantity of {quantity} {name} has/have been sold for the price of {store[name]['price'] :,.2f} each. Total sale price = {total_sale :,.2f}")
# Display inventory
def display_inventory(store):
    print("LIST OF CURRENT INVENTORY")
    for products in store:
        print(f"""
                ___
                |
                |Name: {products},\t\t\t Price: {store[products]['price']},\t\t\t Quantity: {store[products]['quantity']}
                |__
                """)
    print("TOTAL NUMBER OF PRODUCTS")
    total_products = 0
    for products in store:
        total_products += store[products]["quantity"]
    print(f"Total number of products in store = {total_products}")
# Return most expensive product
def most_expensive_product(store):
    highest_price = 0
    for product in store:
        if store[product]["price"] > highest_price:
            highest_price = store[product]["price"]
            print(f"The product with the highest price is {product} and it costs {highest_price}")
# Return total potential sales
def total_potential_sales(store):
    total_price = 0
    for products in store:
        total_price += store[products]["price"] * store[products]["quantity"]
    return total_price

start()
