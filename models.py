from pydantic import BaseModel


class Product(BaseModel): 
    id: int
    name: str
    description: str
    price: float
    quantity: int

    # def __init__(self, id: int, name: str, description: str, price: float, quantity: int):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.price = price
    #     self.quantity = quantity