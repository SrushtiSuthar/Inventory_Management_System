import sys
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFormLayout, QComboBox, QCompleter, QTextEdit, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

# ------------------------- Load Inventory -------------------------
def load_inventory(filepath="Grocery Inventory.json"):
    # Load inventory data from a JSON file
    with open(filepath, "r") as file:
        return json.load(file)

# Store inventory dictionary globally
Inventory = load_inventory()

# ------------------------- Bill Window -------------------------
class BillWindow(QWidget):
    def __init__(self, user_data, item_data, parent=None):
        super().__init__()
        self.parent_window = parent  # Save parent reference
        self.setWindowTitle('Bill')
        self.setGeometry(150, 150, 600, 600)
        self.user_data = user_data
        self.item_data = item_data
        self.inventory = Inventory
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()

        # Title label for the bill window
        title = QLabel('Bill', self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background-color: lightblue; font-weight: bold; font-size: 15px;")
        title.setFixedSize(600, 50)

        bill = QTextEdit(self)
        font = QFont("Courier New")
        bill.setFont(font)
        bill.setReadOnly(True)

        text = ""
        text += "------------------------------GROCERY STORE BILL-------------------------------\n\n"
        text += f"{"Name":<12} : {self.user_data[0]}\n"
        text += f"{"Phone no.":<12} : {self.user_data[1]}\n\n"
        text += "-------------------------------------Order-------------------------------------\n\n"
        text += f"{'Reference No.':<15}{'Product Name':<35}{'Price':<10}{'Quantity':<10}{'Total':<10}\n"
        text += "-" * 79 + "\n"

        bill_items = ""
        for i in self.item_data:
            bill_items += f"{i['Reference No.']:<15}{i['Product Name']:<35}{i['Price']:<10}{i['Quantity']:<10}{float(i['Price']) * int(i['Quantity']):<20.2f}\n"

        text += bill_items

        bill_total = 0
        for i in self.item_data:
            total = int(i['Quantity']) * float(i['Price'])
            bill_total +=total

        text += "\n-------------------------------------------------------------------------------\n"
        text += f"{'Total Bill :':<70}{bill_total}"
        bill.setPlainText(text)

        update_button = QPushButton("Print Bill and Update Inventory")
        update_button.clicked.connect(self.update_inventory)

        layout.addRow(title)
        layout.addRow(bill)
        layout.addRow(update_button)
        self.setLayout(layout)

    def update_inventory(self):
        for i in self.item_data:
            ref_no = i['Reference No.']
            if ref_no in self.inventory:
                self.inventory[ref_no]["Stock_Quantity"] = str(int(self.inventory[ref_no]["Stock_Quantity"]) - int(i['Quantity']))

        with open("Grocery Inventory.json", "w") as file:
            json.dump(self.inventory, file, indent=4)

        self.close()

        if self.parent_window and hasattr(self.parent_window, 'refresh_inventory'):
            self.parent_window.refresh_inventory()

# ------------------------- Grocery Window -------------------------
class GroceryWindow(QWidget):
    # Custom signal to send selected item keys back to main window
    items_selected = Signal(list, list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Grocery List')
        self.setGeometry(150, 150, 500, 500)
        self.Final_items = []  # To store final selected item keys
        self.setup_ui()

    # Defining the other UI widgets
    def setup_ui(self):
        layout = QFormLayout()

        # Title
        title = QLabel('Grocery List', self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background-color: lightblue; font-weight: bold; font-size: 15px;")
        title.setFixedSize(500, 50)

        # Category dropdown
        category_label = QLabel('Select Category:', self)
        self.category_combo = QComboBox(self)
        self.category_combo.addItems([
            "Bakery", "Beverages", "Dairy", "Fruits & Vegetables",
            "Grains & Pulses", "Oils & Fats", "Seafood"
        ])
        self.category_combo.setPlaceholderText("Select category")

        # Items dropdown (dependent on selected category)
        item_label = QLabel('Select item/s from:', self)
        self.item_combo = QComboBox(self)
        self.item_combo.setEditable(True)

        # When category changes, update item list
        self.category_combo.currentIndexChanged.connect(self.update_items)

        # Quantity input
        quantity_label = QLabel('Enter the quantity of the item selected:', self)
        self.ui_quantity = QLineEdit()
        self.ui_quantity.setPlaceholderText("1")

        # Add button
        add_button = QPushButton('Enter the Selected Item', self)
        add_button.clicked.connect(self.selected_item)

        # Text area to show selected items
        self.selected_items = QTextEdit()
        self.selected_items.setPlaceholderText("Your selected items and quantity")

        # Submit button
        submit_button = QPushButton('Submit', self)
        submit_button.clicked.connect(self.final_button)

        # Add widgets to layout
        layout.addRow(title)
        layout.addRow(category_label, self.category_combo)
        layout.addRow(item_label, self.item_combo)
        layout.addRow(quantity_label, self.ui_quantity)
        layout.addRow(add_button)
        layout.addRow(self.selected_items)
        layout.addRow(submit_button)

        self.setLayout(layout)

    def update_items(self):
        # Update items shown based on selected category
        selected_category = self.category_combo.currentText()
        self.item_combo.clear()
        display_items = []

        for key, val in Inventory.items():
            if val["Category"] == selected_category:
                display = f'{val["Product_Name"]} | {val["Unit_Price"]} | {val["Stock_Quantity"]}'
                self.item_combo.addItem(display, userData=int(key))
                display_items.append(display)

        # Add auto-complete to item selector
        completer = QCompleter(display_items, self.item_combo)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.item_combo.setCompleter(completer)
        self.item_combo.setCurrentIndex(-1)
        self.item_combo.lineEdit().setPlaceholderText("Product Name : Price : Quantity")

    def selected_item(self):
        # Add selected item and quantity to the display
        index = self.item_combo.currentIndex()
        item_key = self.item_combo.itemData(index)
        quantity = self.ui_quantity.text().strip()

        if item_key and quantity:
            item = Inventory[str(item_key)]
            self.selected_items.append(
                f"{item_key} : {item['Product_Name']} | {item['Unit_Price']} | {quantity}"
            )

    def final_button(self):
        # Extract only the item keys from selected list and emit signal
        lines = self.selected_items.toPlainText().splitlines()
        Final_items = [line.split(" : ")[0] for line in lines if " : " in line]
        User_quantity = [line.split(" | ")[2] for line in lines if " | " in line]
        self.items_selected.emit(Final_items, User_quantity)
        self.close()

# ------------------------- Main Window -------------------------
class InventoryApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Customer Entry')
        self.setGeometry(50, 50, 500, 500)
        self.inventory = Inventory  # Store inventory
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()

        # Title label
        title = QLabel('Customer Details', self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background-color: lightblue; font-weight: bold; font-size: 15px;")
        title.setFixedSize(500, 50)

        # Labels and input fields for customer name and phone number
        name_label = QLabel('Name :', self)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your Name")

        phone_label = QLabel('Phone No :', self)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("1234567890")

        # Label and button to open GroceryWindow
        select_label = QLabel('Select your items :', self)
        select_button = QPushButton('Grocery', self)
        select_button.clicked.connect(self.open_GroceryWindow)

        # Table to display selected items
        self.grocery_table = QTableWidget(self)
        self.grocery_table.setColumnCount(4)
        self.grocery_table.setHorizontalHeaderLabels(["Reference No.", "Product Name", "Price", "Quantity"])

        # Button to open BillWindow
        bill_button = QPushButton('Generate Bill', self)
        bill_button.clicked.connect(self.open_BillWindow)

        # Add widgets to layout
        layout.addRow(title)
        layout.addRow(name_label, self.name_input)
        layout.addRow(phone_label, self.phone_input)
        layout.addRow(select_label, select_button)
        layout.addRow(self.grocery_table)
        layout.addRow(bill_button)

        self.setLayout(layout)

    def Grocery_table(self, selected_keys, item_quantity):
        # Fill table with selected item details
        self.grocery_table.setRowCount(len(selected_keys))
        for row, key in enumerate(selected_keys):
            item = self.inventory.get(key)
            if item:
                self.grocery_table.setItem(row, 0, QTableWidgetItem(str(key)))
                self.grocery_table.setItem(row, 1, QTableWidgetItem(str(item["Product_Name"])))
                self.grocery_table.setItem(row, 2, QTableWidgetItem(str(item["Unit_Price"])))
                self.grocery_table.setItem(row, 3, QTableWidgetItem(str(item_quantity[row])))

    def open_GroceryWindow(self):
        # Open grocery item selection window
        self.grocery_window = GroceryWindow()
        self.grocery_window.items_selected.connect(self.Grocery_table)
        self.grocery_window.show()

    def open_BillWindow(self):
        # Collect table data directly here
        user_data = [self.name_input.text(), self.phone_input.text()]
        table_data = []
        for row in range(self.grocery_table.rowCount()):
            row_data = {
                "Reference No.": self.grocery_table.item(row, 0).text(),
                "Product Name": self.grocery_table.item(row, 1).text(),
                "Price": self.grocery_table.item(row, 2).text(),
                "Quantity": self.grocery_table.item(row, 3).text(),
            }
            table_data.append(row_data)

        # Pass directly to new window
        self.bill_window = BillWindow(user_data, table_data, parent = self)
        self.bill_window.show()

    def refresh_inventory(self):
        with open("Grocery Inventory.json", "r") as file:
            self.inventory = json.load(file)
        # You can also refresh UI elements like tables here

# ------------------------- Run App -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
