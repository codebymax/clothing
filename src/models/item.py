from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List

from .object import PyObjectId


class ItemModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    brand: str = Field(...)
    category: str = Field(...)
    colors: List[str] = Field(...)
    date_purchased: str = Field(...)
    price: float = Field(...)
    vendor: str = Field(...)
    num_wears: int = Field(...)
    keywords: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "brand": "Uniqlo",
                "category": "t-shirt",
                "colors": ["blue"],
                "date_purchased": "01/01/2021",
                "price": 32.40,
                "vendor": "Uniqlo",
                "num_wears": 5,
                "keywords": ["short sleeve", "t-shirt", "blue", ]
            }
        }

    def get_name(self):
        color = "multicolor" if len(self.colors) > 2 else " ".join(self.colors)
        return self.brand + " " + color + " " + self.category


class UpdateItemModel(BaseModel):
    brand: Optional[str]
    category: Optional[str]
    color: Optional[str]
    date_purchased: Optional[str]
    price: Optional[float]
    vendor: Optional[str]
    num_wears: Optional[str]
    keywords: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "brand": "Uniqlo",
                "category": "t-shirt",
                "colors": ["blue"],
                "date_purchased": "12/11/1998",
                "price": 32.40,
                "vendor": "Uniqlo",
                "keywords": ["short sleeve"]
            }
        }