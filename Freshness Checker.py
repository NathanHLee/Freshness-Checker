from datetime import date, timedelta
from multiprocessing.sharedctypes import Value
import sqlite3

# Connect to the database file to search for information
connection = sqlite3.connect('fridge_inventory.db')
cursor = connection.cursor()

# Create an empty table if there is no file to search
cursor.execute("CREATE TABLE IF NOT EXISTS inventory (name TEXT, purchased TEXT, expiration TEXT, expired TEXT)")

choice = None
# Choice 6 is to quit the program
while choice != "6":
    # Display the menu to the user
    print("1) Display Items in Fridge")
    print("2) Add New Item to Fridge")
    print("3) Update an Item")
    print("4) Remove an Item")
    print("5) Check Items Close to Spoiling")
    print("6) Quit")
    choice = input("> ")
    print()

    # Display Items in Fridge
    if (choice == "1"):
        # Create the header
        cursor.execute("SELECT * FROM inventory ORDER BY purchased DESC")
        print("{:>15}  {:>15}  {:>15}  {:>25}".format("Name", "Purchased", "Expiration", "Expired?"))
        print("------------------------------------------------------------------------------------")
        
        # Selects all information and sort it by date purchased
        for record in cursor.fetchall():
            # Split the expired data and convert it into a useable date
            #   Split the string by the '-' to get an individual day, month, and year
            split_date = record[2].split('-')
            #   Convert those three string types into one new date
            exp_date = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
            #   Subtract the created date with today's date to get days until expriation
            days_left = exp_date - date.today()
            #   Split again to only retrieve the amount of days left
            split_exp_date = str(days_left).split()


            # Check to see if the item is expired
            if (int(split_exp_date[0]) <= 0):
                expired = (f"EXPIRED! {abs(int(split_exp_date[0]))} days past!")
            # Else, print off how many days you have until the item expires
            else:
                expired = str(split_exp_date[0] + " days left")
                
            # Loop through the whole database
            print("{:>15}  {:>15}  {:>15}  {:>25}".format(record[0], record[1], record[2], expired))
        print()

    # Add New Item to Fridge
    elif (choice == "2"):
        print("What item did you purchase?")
        name = input("> ")
        print("Was this purchased today? (Y/N)")
        today_input = input("> ")

        # Get today's date to save the user time
        if (today_input == "Y" or today_input == "y"):
            purchased = date.today()
            print(purchased)
        # If the user forgot to update their fridge on time, they can enter their purchase date
        else:
            print(f"When did you purchase {name}?")
            p_month = int(input('Month: '))
            p_day = int(input('Day: '))
            p_year = int(input('Year: '))
            # Format the string input into a date variable
            purchased = date(p_year, p_month, p_day)
        
        print("What was the expiration date?")
        exp_month = int(input('Month: '))
        exp_day = int(input('Day: '))
        exp_year = int(input('Year: '))
        # Format the string input into a date variable
        expiration = date(exp_year, exp_month, exp_day)

        # Tuple the values together to insert them into the database
        #   The 0 is there because there are 4 columns, but the 4th column is
        #   calculated when the table is retrieved
        values = (name, purchased, expiration, 0)
        cursor.execute("INSERT INTO inventory VALUES (?,?,?,?)", values)
        connection.commit()

    # Update an Item
    elif (choice == "3"):
        try:
            print("What is the item name?")
            name = input("> ")
            print("What is the expiration date")
            exp_month = int(input('Month: '))
            exp_day = int(input('Day: '))
            exp_year = int(input('Year: '))
            # Format the string input into a date variable
            expiration = date(exp_year, exp_month, exp_day)

            values = (expiration, name)
        
            # Check if the given name matches with one in the database
            cursor.execute("UPDATE inventory SET expiration = ? WHERE name = ?", values)
            connection.commit()
            # If there are no rows that match that name
            if cursor.rowcount == 0:
                print("Invalid item!")
        except ValueError:
            print("Invalid date!")

    # Remove an Item
    elif (choice == "4"):
        print("What is the item name?")
        name = input("> ")
        if name == None:
            continue
        values = (name, )
        cursor.execute("DELETE FROM inventory WHERE name = ?", values)
        connection.commit()
        print()

    elif (choice == "5"):
        # Create the header
        cursor.execute("SELECT * FROM inventory ORDER BY expiration ASC")
        print("{:>15}  {:>15}  {:>15}  {:>25}".format("Name", "Purchased", "Expiration", "Expired?"))
        print("------------------------------------------------------------------------------------")
        
        # Selects all information and sort it by date purchased
        for record in cursor.fetchall():
            # Split the expired data and convert it into a useable date
            #   Split the string by the '-' to get an individual day, month, and year
            split_date = record[2].split('-')
            #   Convert those three string types into one new date
            exp_date = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
            #   Subtract the created date with today's date to get days until expriation
            days_left = exp_date - date.today()
            #   Split again to only retrieve the amount of days left
            split_exp_date = str(days_left).split()

            # Check to see if the item is expired
            if (int(split_exp_date[0]) <= 0):
                expired = (f"EXPIRED! {abs(int(split_exp_date[0]))} days past!")
            # Else, print off how many days you have until the item expires
            else:
                expired = str(split_exp_date[0] + " days left")
                
            # Loop through the whole database
            #   Check items that have expired or will expire in the next 5 days
            if (int(split_exp_date[0]) <= 5):    
                print("{:>15}  {:>15}  {:>15}  {:>25}".format(record[0], record[1], record[2], expired))
        print()


# Close the database connection before exiting
connection.close()