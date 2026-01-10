class ProductNotFound(Exception):
    """Raised when a product with given id does not exist."""
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with id={product_id} not found")


class ProductValidationError(Exception):
    """Raised when product validation fails for business rules."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
