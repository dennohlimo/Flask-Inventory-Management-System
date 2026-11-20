import requests

API_URL = "http://127.0.0.1:5000"

def view_all():
    response = requests.get(f"{API_URL}/inventory")

    if response.status_code == 200:
        products = response.json()

        for product in products:
            print("ID:", product["id"])
            print("Name:", product["product_name"])
            print("Brand:", product["brands"])
            print("Price:", product["price"])
            print("Stock:", product["stock"])
            print("----------------")
    else:
        print("unable to get inventory")
def add_inventory():
    product_name = input("Enter product name: ")
    brands = input("Enter brand: ")
    barcode = input("Enter barcode: ")
    ingredients_text = input("Enter ingredients: ")

    try:
        price = float(input("Enter price: "))
        stock = int(input("Enter stock: "))

        product = {
            "product_name": product_name,
            "brands": brands,
            "barcode": barcode,
            "ingredients_text": ingredients_text,
            "price": price,
            "stock": stock
        }
        response = requests.post(
            f"{API_URL}/inventory",
            json=product
        )
        print(response.json())

    except ValueError:
        print("Please enter a valid number for price and stock")

def view_one():
    item_id = input("Item ID: ")
    response = requests.get(f"{API_URL}/inventory/{item_id}")
    if response.status_code == 200:
        print(response.json())
    else:
        print("unable to get item")

def update_item():
    item_id = input("Enter item ID: ")

    try:
        price = input("Enter new price or press enter to skip: ")
        stock = input("Enter new stock or press enter to skip: ")
        updated_data = {}
        if price:
            updated_data["price"] = float(price)
        if stock:
            updated_data["stock"] = int(stock)
        response = requests.patch(
            f"{API_URL}/inventory/{item_id}",
            json=updated_data
        )
        if not updated_data:
            print("No changes were made")
            return
        print(response.json())
    except ValueError:
        print("Please enter a valid number for price or stock")

def delete_item():
    item_id = input("Enter item ID: ")

    response = requests.delete(f"{API_URL}/inventory/{item_id}")

    if response.status_code == 200:
        print(response.json())
    else:
        print("Unable to delete item")

def find_product():
    print("\n Find an item on OpenFoodFacts")
    print("1. Search by barcode")
    print("2. Search by product name")

    choice = input("Choose search method: ")

    if choice == "1":
        barcode = input("Enter product barcode: ")

        response = requests.get(
            f"{API_URL}/inventory/search",
            params={"barcode": barcode}
        )

    elif choice == "2":
        product_name = input("Enter product name: ")

        response = requests.get(
            f"{API_URL}/inventory/search",
            params={"name": product_name}
        )

    else:
        print("Invalid choice")
        return

    if response.status_code == 200:
        print(response.json())
    else:
        print("Unable to find product")
        print("Status code:", response.status_code)
        print("Response:", response.text)

def import_product():
    barcode = input("Enter product barcode: ")
    try:
        price = float(input("Enter product price: "))
        stock = int(input("Enter product stock: "))

        product = {
            "barcode": barcode,
            "price": price,
            "stock": stock
        }

        response = requests.post(
            f"{API_URL}/inventory/import",
            json=product
        )

        if response.status_code == 201:
            print(response.json())
        else:
            print("Unable to import product")
            print(response.json())

    except ValueError:
        print("Please enter a valid price and stock")
        
def main():
    while True:
        print("\n=== Inventory Management CLI ===")
        print("1. Add inventory item")
        print("2. View all inventory")
        print("3. View one item")
        print("4. Update price or stock")
        print("5. Delete product")
        print("6. Find product on OpenFoodFacts")
        print("7. Import product from OpenFoodFacts")
        print("0. Exit")

        choice = input("Please enter your option: ")

        if choice == "1":
            add_inventory()
        elif choice == "2":
            view_all()
        elif choice == "3":
            view_one()
        elif choice == "4":
            update_item() 
        elif choice == "5":
            delete_item()
        elif choice == "6":
            find_product()
        elif choice == "7":
            import_product()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
