from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")
async def greet():
    return {"Hello": "World"}

products = [
    Product(id = 1, name = "Sample Product", description = "This is a sample product", price = 19.99, quantity = 100), 
    Product(id = 2, name = "Another Product", description = "This is another product", price = 29.99, quantity = 50),
    Product(id = 3, name = "Third Product", description = "This is the third product", price = 9.99, quantity = 200)
]

@app.get("/products")
async def get_products():
    return {"all products": products}

@app.get("/products/{product_id}")

def get_product_by_id(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return None

@app.post("/products")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for index, product in enumerate(products):
        if product.id == product_id:
            products[index] = updated_product
            return updated_product
    return None