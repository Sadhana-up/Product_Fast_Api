from fastapi import FastAPI
from models import Product
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()


database_models.Base.metadata.create_all(bind=engine)
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
    #db connect garne : 
    db = session()
    # query garne 
    db.query()


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


@app.get("/whoami")
def whoami():
    import multiprocessing
    return {
        "pid": os.getpid(),
        "ppid": os.getppid(),  # Parent process ID
        "worker_name": multiprocessing.current_process().name,
        "is_main": multiprocessing.current_process().name == "MainProcess"
    }

if __name__ == "__main__":
    import uvicorn
    
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # Convertin to python BOOL
    ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV").upper()  
    
    
    if ENVIRONMENT == "PROD":
        WORKERS = int(os.getenv("WORKERS", 1))  
        print(f"Starting in PROD mode with {WORKERS} workers")
        
        uvicorn.run(
            "main:app",  
            host=HOST,
            port=PORT,
            workers=WORKERS,    
            log_level="info",
            access_log=True
        )
    else:
        uvicorn.run(
            "main:app",  
            host=HOST,
            port=PORT,
            reload=True,  
            log_level="debug",
            access_log=True,
            use_colors=True
        )
