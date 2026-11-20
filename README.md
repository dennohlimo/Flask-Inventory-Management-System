# Flask-Inventory-Management-System# Flask Inventory Management System

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Local Setup](#local-setup)
- [API Reference](#api-reference)
- [CLI Usage Guide](#cli-usage-guide)
- [Troubleshooting](#troubleshooting)
- [Known Issues](#known-issues)
- [Potential Improvements](#potential-improvements)
- [Data Source](#data-source)

## Overview
**Flask Inventory Management System** is an administrator portal for managing the product inventory of an e-commerce website. It has two parts that run side by side: a **Flask REST API** that stores and changes the inventory, and a **menu-driven command-line program** that talks to that API. The API can also look products up on [Open Food Facts](https://world.openfoodfacts.org) by barcode or name and import them into the inventory, so an administrator only has to add a price and a stock level.

The inventory is kept in a Python list while the server is running, so it starts from five sample products each time the server is started.

### Purpose
- Practice building a REST API with Flask: routes, HTTP methods, JSON requests and responses, and status codes
- Practice connecting to an external API (Open Food Facts) and using its data in your own program
- Practice building a command-line client that talks to an API over HTTP
- Practice splitting a program into separate files that depend on each other

## Features

### Core Features
- **View Inventory** — list every product, or look up one product by its ID
- **Add Products** — create a product with a name, price and stock level, and optionally a brand, barcode and ingredients
- **Update Products** — the API can change any detail of a product, and the CLI changes a product's price or stock level
- **Delete Products** — remove a product by its ID
- **Find Products on Open Food Facts** — look a product up by barcode or by name
- **Import Products** — add a product to the inventory from its barcode; its name, brand and ingredients are filled in from Open Food Facts, and you supply the price and stock
- **Duplicate Check on Import** — a product whose barcode is already in the inventory is refused

### User Experience Features
- **Menu-Driven Interface** — a numbered menu that repeats until the user chooses `0` to exit
- **Number Checks** — if the price or stock is not a number, the CLI shows a message instead of crashing
- **Clear Error Messages** — the API replies with a short JSON message and a status code such as `404` or `409` when something goes wrong
- **CORS Enabled** — a web page on another address can call the API

## Technologies Used

### Language
- **Python 3** — developed with Python 3.14

### Third-Party Packages
- **Flask** — the web framework that provides the routes
- **flask-cors** — allows the API to be called from web pages on other addresses
- **openfoodfacts** — the official Open Food Facts Python SDK, used in `food_api.py`
- **requests** — used by the CLI to send HTTP requests to the API

The exact versions are listed in `requirements.txt`.

### Tools
- **Postman** or **curl** — useful for trying the API endpoints directly

## Project Structure

```
Flask-Inventory-Management-System/
├── app.py              # the Flask API: all routes and the in-memory inventory
├── food_api.py         # functions that look products up on Open Food Facts
├── cli.py              # the menu-driven command-line program
├── requirements.txt    # packages to install
└── README.md
```

- `app.py` holds the `inventory` list and every route. It imports two functions from `food_api.py`
- `food_api.py` creates the Open Food Facts client and provides `search_by_barcode()` and `search_by_name()`
- `cli.py` never touches the inventory itself. Each menu option sends a request to the API and prints the answer

Every product in the inventory is a dictionary with these fields:

| Field | Type | Description |
|---|---|---|
| `id` | whole number | assigned automatically, starting at 1 |
| `product_name` | text | the product's name |
| `brands` | text | the brand, or an empty string |
| `barcode` | text | the barcode, or an empty string |
| `price` | number | the selling price |
| `stock` | whole number | how many are in stock |
| `ingredients_text` | text | the ingredients, or an empty string |

## Local Setup

### Requirements
- Python 3 (developed with Python 3.14)
- An internet connection, for the Open Food Facts lookups
- A terminal or command prompt

### Installation
1. Clone the repository:
   ```
   git clone <your-repo-url>
   ```
2. Go into the project folder:
   ```
   cd Flask-Inventory-Management-System
   ```
3. Create a virtual environment:
   ```
   python3 -m venv .venv
   ```
4. Activate it:
   ```
   source .venv/bin/activate
   ```
   On Windows, use `.venv\Scripts\activate` instead.
5. Install the packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Program
The API and the CLI run in **two separate terminals**. Start the API first, because the CLI needs it.

**Terminal 1 — the API**
```
python app.py
```
Wait for a line saying `Running on http://127.0.0.1:5000`, and leave this terminal open. The server runs in debug mode, so it restarts by itself whenever you save a change to a file.

**Terminal 2 — the CLI**
```
python cli.py
```
Activate the virtual environment in this terminal too. Press `Ctrl+C` in Terminal 1 to stop the API.

The CLI expects the API at `http://127.0.0.1:5000`. This address is set at the top of `cli.py` as `API_URL`.

## API Reference

The API sends and receives JSON. The base URL is `http://127.0.0.1:5000`. When sending data, set the header `Content-Type: application/json`. Responses list their fields in alphabetical order.

| Method | Endpoint | Purpose | Success |
|---|---|---|---|
| `GET` | `/inventory` | Fetch all products | `200` |
| `GET` | `/inventory/<id>` | Fetch one product | `200` |
| `POST` | `/inventory` | Add a product | `201` |
| `PATCH` | `/inventory/<id>` | Update a product | `200` |
| `DELETE` | `/inventory/<id>` | Remove a product | `200` |
| `GET` | `/inventory/search` | Find a product on Open Food Facts | `200` |
| `POST` | `/inventory/import` | Import a product from Open Food Facts | `201` |

`GET /` also returns a simple "Home" page.

### Get All Products
`GET /inventory` returns a list of every product.
```
curl http://127.0.0.1:5000/inventory
```
```json
[
  {
    "barcode": "0619209900018",
    "brands": "NutriHarvest",
    "id": 1,
    "ingredients_text": "Macadamia nuts, filtered water, natural sweetener",
    "price": 450.0,
    "product_name": "Kenyan Premium Macadamia Milk",
    "stock": 32
  },
  ...
]
```

### Get One Product
`GET /inventory/<id>` returns one product.
```
curl http://127.0.0.1:5000/inventory/1
```
Returns the product as above. If there is no product with that ID, the status is `404`:
```json
{ "error": "Item not found" }
```

### Add a Product
`POST /inventory` creates a product. `product_name`, `price` and `stock` are required. `brands`, `barcode` and `ingredients_text` are optional.
```
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Oat Milk", "brands": "Oatly", "barcode": "6161101234567", "ingredients_text": "Oats, water", "price": 320.5, "stock": 30}'
```
Status `201`:
```json
{
  "message": "Product added successfully",
  "product": {
    "barcode": "6161101234567",
    "brands": "Oatly",
    "id": 6,
    "ingredients_text": "Oats, water",
    "price": 320.5,
    "product_name": "Oat Milk",
    "stock": 30
  }
}
```
If a required field is missing, the status is `400`:
```json
{ "message": "Missing required fields: price, stock" }
```
If no data is sent at all, the status is `400` with `{ "error": "Please provide product details" }`.

### Update a Product
`PATCH /inventory/<id>` changes only the fields you send. Any of `product_name`, `brands`, `barcode`, `price`, `stock` and `ingredients_text` can be sent.
```
curl -X PATCH http://127.0.0.1:5000/inventory/6 \
  -H "Content-Type: application/json" \
  -d '{"price": 350, "stock": 28}'
```
Status `200`:
```json
{
  "message": "Product 'Oat Milk' updated successfully",
  "product": {
    "barcode": "6161101234567",
    "brands": "Oatly",
    "id": 6,
    "ingredients_text": "Oats, water",
    "price": 350,
    "product_name": "Oat Milk",
    "stock": 28
  }
}
```
Errors: `400` with `{ "error": "Please provide product details" }` if no data is sent, and `404` with `{ "error": "Product not found" }` if the ID does not exist.

### Delete a Product
`DELETE /inventory/<id>` removes a product.
```
curl -X DELETE http://127.0.0.1:5000/inventory/6
```
Status `200`:
```json
{ "message": "Product 'Oat Milk' deleted successfully" }
```
If the ID does not exist, the status is `404` with `{ "error": "Item not found" }`.

### Find a Product on Open Food Facts
`GET /inventory/search` looks a product up on Open Food Facts without changing the inventory. Give either `barcode` or `name` as a query parameter. If both are given, the barcode is used.
```
curl "http://127.0.0.1:5000/inventory/search?barcode=3017620422003"
```
Status `200`:
```json
{
  "brands": "Ferrero, Nutella",
  "code": "3017620422003",
  "ingredients_text": "sugar, palm oil",
  "product_name": "Nutella"
}
```
Errors: `400` with `{ "error": "Please enter a barcode or product name" }` if neither parameter is given, and `404` with `{ "error": "Item not found" }` if nothing matches.

Searching by name works the same way (`/inventory/search?name=nutella`), but see [Known Issues](#known-issues) first.

### Import a Product
`POST /inventory/import` looks a product up by barcode on Open Food Facts and adds it to the inventory. Its name, brand, barcode and ingredients come from Open Food Facts. `barcode` is required. `price` and `stock` are optional and both default to `0`.
```
curl -X POST http://127.0.0.1:5000/inventory/import \
  -H "Content-Type: application/json" \
  -d '{"barcode": "3017620422003", "price": 540, "stock": 12}'
```
Status `201`:
```json
{
  "message": "Product imported successfully",
  "product": {
    "barcode": "3017620422003",
    "brands": "Ferrero, Nutella",
    "id": 6,
    "ingredients_text": "sugar, palm oil",
    "price": 540,
    "product_name": "Nutella",
    "stock": 12
  }
}
```

| Status | Body | Meaning |
|---|---|---|
| `400` | `{ "error": "Please provide a barcode" }` | no barcode was sent |
| `404` | `{ "error": "Product not found" }` | Open Food Facts has no product with that barcode |
| `409` | `{ "error": "Product already exists in inventory" }` | a product with that barcode is already in the inventory |

### Trying the API in Postman
Choose the method, enter the URL, and for `POST` and `PATCH` open **Body**, choose **raw** and **JSON**, and paste the JSON from the examples above.

## CLI Usage Guide

Start the API first, then run `python cli.py`. The program shows this menu:

```
=== Inventory Management CLI ===
1. Add inventory item
2. View all inventory
3. View one item
4. Update price or stock
5. Delete product
6. Find product on OpenFoodFacts
7. Import product from OpenFoodFacts
0. Exit
```

Type a number and press Enter. After each action the menu appears again.

### Adding an Item
1. Choose **1**
2. Enter the product name, brand, barcode and ingredients. The brand, barcode and ingredients can be left empty by pressing Enter
3. Enter the price (a number such as `4.99`) and the stock (a whole number such as `20`). If either is not a number, the program tells you and returns to the menu
4. The program prints the API's reply, which includes the new product and its ID

### Viewing All Inventory
1. Choose **2**
2. Every product is printed with its ID, name, brand, price and stock

### Viewing One Item
1. Choose **3**
2. Enter the item ID. The product's full details are printed

### Updating Price or Stock
1. Choose **4**
2. Enter the item ID
3. Enter a new price, a new stock level, or both. Press Enter to skip one

### Deleting a Product
1. Choose **5**
2. Enter the item ID. The product is removed straight away, without asking for confirmation

### Finding a Product on Open Food Facts
1. Choose **6**
2. Choose **1** to search by barcode or **2** to search by product name
3. Enter the barcode or the name. The product details are printed, and nothing is added to the inventory

### Importing a Product from Open Food Facts
1. Choose **7**
2. Enter the product's barcode, then the price and stock you want to record
3. The product's name, brand and ingredients are fetched from Open Food Facts and the product is added to the inventory
4. A barcode that is already in the inventory is refused

### Exiting
1. Choose **0**

### Example Session
The list of menu options is left out below to keep it short, and the middle of the inventory list is shortened. Results are printed as Python dictionaries.
```
Please enter your option: 1
Enter product name: Oat Milk
Enter brand: Oatly
Enter barcode: 6161101234567
Enter ingredients: Oats, water
Enter price: 320.5
Enter stock: 30
{'message': 'Product added successfully', 'product': {'barcode': '6161101234567', 'brands': 'Oatly', 'id': 6, 'ingredients_text': 'Oats, water', 'price': 320.5, 'product_name': 'Oat Milk', 'stock': 30}}

Please enter your option: 3
Item ID: 6
{'barcode': '6161101234567', 'brands': 'Oatly', 'id': 6, 'ingredients_text': 'Oats, water', 'price': 320.5, 'product_name': 'Oat Milk', 'stock': 30}

Please enter your option: 4
Enter item ID: 6
Enter new price or press enter to skip: 350
Enter new stock or press enter to skip:
{'message': "Product 'Oat Milk' updated successfully", 'product': {'barcode': '6161101234567', 'brands': 'Oatly', 'id': 6, 'ingredients_text': 'Oats, water', 'price': 350.0, 'product_name': 'Oat Milk', 'stock': 30}}

Please enter your option: 6

 Find an item on OpenFoodFacts
1. Search by barcode
2. Search by product name
Choose search method: 1
Enter product barcode: 3017620422003
{'brands': 'Ferrero, Nutella', 'code': '3017620422003', 'ingredients_text': 'sugar, palm oil', 'product_name': 'Nutella'}

Please enter your option: 7
Enter product barcode: 3017620422003
Enter product price: 540
Enter product stock: 12
{'message': 'Product imported successfully', 'product': {'barcode': '3017620422003', 'brands': 'Ferrero, Nutella', 'id': 7, 'ingredients_text': 'sugar, palm oil', 'price': 540.0, 'product_name': 'Nutella', 'stock': 12}}

Please enter your option: 5
Enter item ID: 6
{'message': "Product 'Oat Milk' deleted successfully"}

Please enter your option: 2
ID: 1
Name: Kenyan Premium Macadamia Milk
Brand: NutriHarvest
Price: 450.0
Stock: 32
----------------
...
ID: 7
Name: Nutella
Brand: Ferrero, Nutella
Price: 540.0
Stock: 12
----------------

Please enter your option: 0
Goodbye!
```
Restarting the API puts the inventory back to the five sample products.

## Troubleshooting

- **`Connection refused` or `ConnectionError` in the CLI** — the API is not running. Start it with `python app.py` in another terminal and wait for `Running on http://127.0.0.1:5000`
- **`ModuleNotFoundError` or `ImportError` when starting either program** — the virtual environment is not active, or the packages are not installed. Activate it and run `pip install -r requirements.txt`
- **The API stops after you save a file** — debug mode restarts the server on every save, and a mistake in the saved file stops it. Read the error in Terminal 1, fix it and save again
- **A lookup fails with a server error** — check your internet connection. Open Food Facts also limits how many requests it accepts (see [Data Source](#data-source)), so wait a minute and try again

## Known Issues
- **Data is not saved.** The inventory lives in memory, so every change is lost when the API stops and the five sample products come back
- **Searching by name is unreliable.** It did not work consistently when the project was tested. It also returns Open Food Facts' full response instead of one product, replies `200` even when nothing matches, and reports a failed search as "Item not found". Searching by barcode is the dependable way to find a product
- **A failed barcode lookup shows an error page.** If Open Food Facts or the internet connection fails during a barcode search or an import, the API replies with Flask's HTML error page (status `500`) instead of a JSON message
- **The API does not check price or stock.** Text or negative values sent straight to the API are stored. Only the CLI checks that the values are numbers
- **A product can be updated to a blank name or to a barcode that is already in use**, and adding a product by hand does not check for a duplicate barcode
- **The duplicate check on import compares the typed barcode only.** The same product written with a different number of leading zeros can be imported twice
- **IDs can be reused.** If the product with the highest ID is deleted, the next new product gets that ID again
- **One error message uses a different key.** Missing required fields on `POST /inventory` returns `"message"` where every other error returns `"error"`
- **No login and no confirmation.** Anyone who can reach the API can change the inventory, the CLI deletes without asking, and the API accepts requests from any web page. Debug mode is on, so run it on your own computer only
- **No automated tests yet**

## Potential Improvements
- **Save the Inventory** — keep the data in a JSON file or a database so it survives a restart
- **Fix Name Search** — return one clean product, or a short list to choose from, report "not found" correctly, and make it work reliably
- **Handle Lookup Failures** — return a clear JSON error when Open Food Facts cannot be reached
- **Validate Input in the API** — reject text or negative prices and stock levels, blank names and duplicate barcodes
- **Fill in Existing Products** — add a route and a menu option that fills a product's blank details from Open Food Facts using its barcode
- **Import by Name** — let the user pick one of several matches and import it
- **Ask Before Deleting** — confirm in the CLI before removing a product
- **Login** — require an administrator password before the inventory can be changed
- **Automated Tests** — add `pytest` tests for the routes, the CLI and the Open Food Facts functions, with the external API mocked

## Data Source
Product information comes from [Open Food Facts](https://world.openfoodfacts.org), a database made by volunteers and available under the [Open Database License](https://opendatacommons.org/licenses/odbl/1.0/). Open Food Facts asks every application to send a custom `User-Agent`, which is set in `food_api.py` as `InventoryManager/1.0`; adding a contact email in brackets, for example `InventoryManager/1.0 (you@example.com)`, is recommended. It also limits each IP address to about 15 product lookups and 10 searches per minute. See the [Open Food Facts API documentation](https://openfoodfacts.github.io/openfoodfacts-server/api/) for details.
