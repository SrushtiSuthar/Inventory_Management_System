import Import_all as IA

#def Inventory_update():

#def Sales_update():

#def User_input():

#def main():


Inventory = open("Grocery Inventory.json" , "r")
js = Inventory.read()
Inventory.close()

Inventory = IA.json.loads(js) # Converting the json file to dictionary
# print(record)
# Printing the menu
print("------------------Menu------------------\n")

for key in Inventory:
  print(key , ":" , Inventory[key]["Product_Name"], "|" , Inventory[key]["Unit_Price"], "|" , Inventory[key]["Stock_Quantity"])


# Taking the order as user input
print("\n-----------------Order------------------\n")

ui_name  = str(input("Enter your Name               : "))
ui_phone = str(input("Enter your Phone number       : "))
ui_pr_id = str(input("Enter the Reference number    : "))
ui_pr_qn = int(input("Enter the Quantity you want   : "))

# User input and inventory management
if ui_pr_qn <= Inventory[ui_pr_id]["Stock_Quantity"]:

  # Printing the bill
  print("\n------------------Bill------------------\n")
  print("Name               : " , Inventory[ui_pr_id]["Product_Name"])
  print("Price              : " , Inventory[ui_pr_id]["Unit_Price"])
  print("Quantity           : " , ui_pr_qn)
  print("----------------------------------------")
  print("Billing Amount     : " , int(Inventory[ui_pr_id]["Unit_Price"]) * int(ui_pr_qn))
  print("----------------------------------------\n")

  # Updating the dictionary
  Inventory[ui_pr_id]["Stock_Quantity"] = Inventory[ui_pr_id]["Stock_Quantity"] - ui_pr_qn

  # Sale = ui_name + "," + ui_email + "," + ui_phone + "," + ui_pr_id + "," + str(ui_pr_qn) + "," + str(record[ui_pr_id]["Price"]) + "," + str(record[ui_pr_id]["Price"] * ui_pr_qn) + "," + IA.time.ctime() + "\n"

else:
  print("Sorry, currently we only have " + str(Inventory[ui_pr_id]["Stock_Quantity"]) + " left in quantity.")
  bc = input("Would you like to buy those? Enter Y(yes) or N(no)")

  if bc == "Y" or bc == "y" or bc == "Yes" or bc == "yes":

    # Printing the bill
    print("\n------------------Bill------------------\n")
    print("Name               : " , Inventory[ui_pr_id]["Product_Name"])
    print("Price              : " , Inventory[ui_pr_id]["Unit_Price"])
    print("Quantity           : " , Inventory[ui_pr_id]["Stock_Quantity"])
    print("----------------------------------------")
    print("Billing Amount     : " , Inventory[ui_pr_id]["Unit_Price"] * Inventory[ui_pr_id]["Stock_Quantity"])
    print("----------------------------------------\n")

    # Updating the dictionary
    Inventory[ui_pr_id]["Stock_Quantity"] = 0

    # Sale = ui_name + "," + ui_email + "," + ui_phone + "," + ui_pr_id + "," + str(ui_pr_qn) + "," + str(record[ui_pr_id]["Price"]) + "," + str(record[ui_pr_id]["Price"] * ui_pr_qn) + "," + IA.time.ctime() + "\n"

# Updating the json file
js = IA.json.dumps(Inventory) # json file stores the data in form of a string
Record = open("Grocery Inventory.json" , "w") # Adding the json to the file, using file handling
Record.write(js)
Record.close()

'''
Sales = open("Sales.txt" , "a")
Sales.write(Sale)
Sales.close()
'''