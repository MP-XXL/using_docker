import time

pin = "*556#"
airtime_balance = 1000
while True:
    #print("Dial *556# for self service")
    dial = input("Dial *556# for self service  or 5 to cancel: ")
    if dial == pin:
        #dial_input = int(input("Choose number to carry out action: \n1. Buy Airtime \n2. Buy Data \n3. Borrow Data \n4. Check Balance \n5. Quit \n >>>>: "))
        action = True
        while action:
            dial_input = input("Choose number to carry out action: \n1. Buy Airtime \n2. Buy Data \n3. Borrow Data \n4. Check Balance \n5. Quit \n >>>>: ")
            if dial_input == "1":
                recharge_amount = int(input("Please input amount of airtime you wish to purchase : "))
                airtime_balance += recharge_amount
                print("Recharging your phone with {:,.2f} airtime".format(recharge_amount))
                time.sleep(2)
                print("Recharge Successful!")
                print("Your new balance is ", airtime_balance)
            elif dial_input == "2":
                data = True
                while data:
                    data_option = int(input("Select option to carry out action:\n1. 1000 for 1GB\n2. 2000 for 3.5GB\n3. 3000 for 8GB\n>>>: "))
                    if data_option == 1:
                        data_price = 1000
                        if data_price <= airtime_balance:
                            airtime_balance -= data_price
                            print(f"Your just bought 1GB data for {data_price:,.2f}, your balance is {airtime_balance:,.2f}")
                        elif data_price  > airtime_balance:
                            print("Insufficient funds")
                    elif data_option == 2:
                        data_price = 2000
                        if data_price <= airtime_balance:
                            airtime_balance -= data_price
                            print(f"Your just bought 3.5G data for {data_price:,.2f}, your balance is {airtime_balance:,.2f}")
                        elif data_price  > airtime_balance:
                            print("Insufficient funds")
                    elif data_option == 3:
                        data_price = 3000
                        if data_price <= airtime_balance:
                            airtime_balance -= data_price
                            print(f"Your just bought 8GB data for {data_price:,.2f}, your balance is {airtime_balance:,.2f}")
                        elif data_price  > airtime_balance:
                            print("Insufficient funds")
                    else:
                        print("Invalid input")
                    data = False
            elif dial_input == "3":
                borrow = True
                while borrow:
                    borrow_option = int(input("Select option to carry out transaction:\n1. To borrow airtime\n2. To borrow data\n>>> : "))
                    if borrow_option == 1:
                        borrow_airtime = True
                        while borrow_airtime:
                            borrow_airtime_option = int(input("Select option to borrow airtime:\n1. To borrow 1000\n2. To borrow 2000\n3. To borrow 3000\n>>> : "))
                            if borrow_airtime_option == 1:
                                borrowed_balance = 1000
                                new_airtime_balance = airtime_balance + borrowed_balance
                                print(f"You just borrowed {borrowed_balance} airtime")
                                print(f"You new balance is {new_airtime_balance:,.2f}")
                                airtime_balance -= new_airtime_balance
                                print(f"Your actual balance is {airtime_balance}")
                                borrow_airtime = False
                                borrow = False
                            if borrow_airtime_option == 2:
                                borrowed_balance = 2000
                                new_airtime_balance = airtime_balance + borrowed_balance
                                print(f"You just borrowed {borrowed_balance} airtime")
                                print(f"You new balance is {new_airtime_balance:,.2f}")
                                airtime_balance -= new_airtime_balance
                                print(f"Your actual balance is {airtime_balance}")
                                borrow_airtime = False
                                borrow = False
                            if borrow_airtime_option == 3:
                                borrowed_balance = 3000
                                new_airtime_balance = airtime_balance + borrowed_balance
                                print(f"You just borrowed {borrowed_balance} airtime")
                                print(f"You new balance is {new_airtime_balance:,.2f}")
                                airtime_balance -= new_airtime_balance
                                print(f"Your actual balance is {airtime_balance}")
                                borrow_airtime = False
                                borrow = False
                            else:
                                print("Invalid Input")
                    if borrow_option == 2:
                        borrow_data = True
                        while borrow_data:
                            borrow_data_option = int(input("Select option to borrow airtime:\n1. To borrow 1GB for 1000\n2. To borrow 3.5GB for 2000\n3. To borrow 8GB for 3000\n>>> : "))
                            if borrow_data_option == 1:
                                borrowed_balance = 1000
                                new_airtime_balance = airtime_balance + borrowed_balance
                                print(f"You just borrowed 1GB data for {borrowed_balance}")
                                airtime_balance -= new_airtime_balance
                                print(f"Your actual balance is {airtime_balance}")
                                borrow_data = False
                                borrow = False
                            if borrow_data_option == 2:
                                borrowed_balance = 2000
                                new_airtime_balance = airtime_balance + borrowed_balance
                                print(f"You just borrowed 3.5GB data for {borrowed_balance}")
                                airtime_balance -= new_airtime_balance
                                print(f"Your actual balance is {airtime_balance}")
                                borrow_data = False
                                borrow = False
                            if borrow_data_option == 3:
                                borrowed_balance =3000
                                new_airtime_balance = airtime_balance + borrowed_balance
                                print(f"You just borrowed 8GB data for {borrowed_balance}")
                                airtime_balance -= new_airtime_balance
                                print(f"Your actual balance is {airtime_balance}")
                                borrow_data = False
                                borrow = False
                            else:
                                print("Invalid input!")
            elif dial_input == "4":
                print(f"Your airtime balance is {airtime_balance}")
            elif dial_input == "5":
                break
            else:
                print("Input unrecognized!")
        break
    elif dial == "5":
        print("Canceling USSD operation...")
        time.sleep(1)
        print("...")
        time.sleep(1)
        print("Operation cancelled")
        break
    else:
        print("Please dial the correct code! : ")
