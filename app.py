import motor.motor_asyncio
from fastapi import FastAPI
import src.routers.items as items
import src.routers.outfits as outfits
import src.routers.categories as categories

uri = "mongodb+srv://rootUser:kgAFR6FP5JBzlT2n@main-xz1r5.mongodb.net/clothingDB?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.clothingDB

app = FastAPI()

app.include_router(outfits.router)
app.include_router(items.router)
app.include_router(categories.router)
