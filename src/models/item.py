from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List

from .misc import PyObjectId


class ItemModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    brand: str = Field(...)
    type: str = Field(...)
    colors: List[str] = Field(...)
    date_purchased: str = Field(...)
    price: float = Field(...)
    vendor: str = Field(...)
    keywords: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "brand": "Uniqlo",
                "type": "t-shirt",
                "colors": ["blue"],
                "date_purchased": "12/11/1998",
                "price": 32.40,
                "vendor": "Uniqlo",
                "keywords": ["short sleeve"]
            }
        }

    def get_name(self):
        color = "multicolor" if len(self.colors) > 2 else " ".join(self.colors)
        return self.brand + " " + color + " " + self.type


class UpdateItemModel(BaseModel):
    brand: Optional[str]
    type: Optional[str]
    color: Optional[str]
    date_purchased: Optional[str]
    price: Optional[float]
    vendor: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "brand": "Uniqlo",
                "type": "t-shirt",
                "colors": ["blue"],
                "date_purchased": "12/11/1998",
                "price": 32.40,
                "vendor": "Uniqlo",
                "keywords": ["short sleeve"]
            }
        }