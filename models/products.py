from typing import Any
from pydantic import BaseModel, field_validator


class Product(BaseModel):
    """Product model with field validators """

    id: int
    name: str
    description: str
    price: float
    quantity: int

    @field_validator("id")
    def id_must_be_positive(cls, v: int) -> int:  
        if v <= 0:
            raise ValueError("id must be a positive integer")
        return v

    @field_validator("name")
    def name_must_not_be_empty(cls, v: str) -> str:  
        v = v.strip()
        if not v:
            raise ValueError("name must not be empty")
        return v

    @field_validator("price")
    def price_must_be_non_negative(cls, v: float) -> float:  
        if v < 0:
            raise ValueError("price must be >= 0")
        return v

    @field_validator("quantity")
    def quantity_must_be_non_negative(cls, v: int) -> int:  
        if v < 0:
            raise ValueError("quantity must be >= 0")
        return v

    model_config = {"from_attributes": True}