from typing import List

import motor.motor_asyncio
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.models import OutfitModel

uri = "mongodb+srv://rootUser:iowastatemongo@main-xz1r5.mongodb.net/clothingDB?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.clothingDB
app = FastAPI()



