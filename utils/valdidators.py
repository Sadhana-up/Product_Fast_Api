from typing import List
from models import Product
from utils.exceptions import ProductValidationError


def validate_new_product(product: Product, existing: List[Product]):
    """Validate business rules when creating a new product.

    Raises ProductValidationError on violation.
    """
    if any(p.id == product.id for p in existing):
        raise ProductValidationError(f"product with id={product.id} already exists", 409)

    if any(p.name.lower() == product.name.lower() for p in existing):
        raise ProductValidationError(f"product with name='{product.name}' already exists", 409)



def validate_update_product(product_id: int, updated: Product, existing: List[Product]):
    """Validate business rules when updating an existing product.

    Raises ProductValidationError on violation.
    """
    if updated.id != product_id:
        raise ProductValidationError("product id in body must match path id", 400)

    for p in existing:
        if p.id != product_id and p.name.lower() == updated.name.lower():
            raise ProductValidationError(f"another product with name='{updated.name}' exists", 409)
