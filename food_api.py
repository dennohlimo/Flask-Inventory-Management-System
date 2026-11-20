import openfoodfacts

food_api = openfoodfacts.API(
    user_agent="InventoryManager/1.0"
)

def search_by_barcode(barcode):
    item = food_api.product.get(barcode, fields=["code","product_name","brands", "ingredients_text"])

    return item

def search_by_name(product_name):
    try:
        item = food_api.product.text_search(product_name, page_size=1)
        return item

    except Exception as error:
        print("Name search error:", error)
        return None