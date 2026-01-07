from typing import Any, Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models import Product
from utils.exceptions import ProductNotFound, ProductValidationError
from utils.valdidators import validate_new_product, validate_update_product
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

@app.get("/")
async def greet():
    return {"Hello": "World"}

products: List[Product] = [
    Product(id=1, name="Sample Product", description="This is a sample product", price=19.99, quantity=100),
    Product(id=2, name="Another Product", description="This is another product", price=29.99, quantity=50),
    Product(id=3, name="Third Product", description="This is the third product", price=9.99, quantity=200),
]

@app.get("/products")
async def get_products() -> Dict[str, List[Product]]:
    return {"all products": [p.model_dump() for p in products]}

@app.get("/products/{product_id}")

def get_product_by_id(product_id: int) -> Product:
    for product in products:
        if product.id == product_id:
            return product
    raise ProductNotFound(product_id)

@app.post("/products")
def add_product(product: Product) -> JSONResponse:
    validate_new_product(product, products)
    products.append(product)
    return JSONResponse(status_code=201, content=product.model_dump())

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product) -> Product:
    for index, product in enumerate(products):
        if product.id == product_id:
            validate_update_product(product_id, updated_product, products)
            products[index] = updated_product
            return updated_product
    raise ProductNotFound(product_id)


@app.exception_handler(ProductNotFound)
async def product_not_found_handler(request: Request, exc: ProductNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"error": str(exc)})


@app.exception_handler(ProductValidationError)
async def product_validation_exception_handler(request: Request, exc: ProductValidationError) -> JSONResponse:
    return JSONResponse(status_code=getattr(exc, "status_code", 400), content={"error": exc.message})


@app.get("/whoami")
def whoami() -> Dict[str, Any]:
    import multiprocessing
    return {
        "pid": os.getpid(),
        "ppid": os.getppid(),
        "worker_name": multiprocessing.current_process().name,
        "is_main": multiprocessing.current_process().name == "MainProcess",
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