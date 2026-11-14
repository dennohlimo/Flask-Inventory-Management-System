


def main():
    while True:
        print("\n=== Inventory Management CLI ===")
        print("1. Add inventory item")
        print("2. View all inventory")
        print("3. View one item")
        print("4. Update price or stock")
        print("5. Delete product")
        print("6. Find product on OpenFoodFacts")
        print("0. Exit")

        choice = input("Please enter your option: ")

        if choice == "1":
            print("Add inventory item")
        elif choice == "2":
            print("View all inventory")
        elif choice == "3":
            print("View one item")
        elif choice == "4":
            print("Update price or stock")
        elif choice == "5":
            print("Delete product")
        elif choice == "6":
            print("Find product on OpenFoodFacts")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
