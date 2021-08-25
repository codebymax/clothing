from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List

from .misc import PyObjectId


class OutfitModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    items: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "items": [
                    "fake_item_id"
                ]
            }
        }


class UpdateOutfitModel(BaseModel):
    items: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "items": [
                    "fake_item_id"
                ]
            }
        }