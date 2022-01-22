from fastapi import FastAPI
import src.routers.items as items
import src.routers.outfits as outfits
import src.routers.categories as categories

app = FastAPI()

app.include_router(outfits.router)
app.include_router(items.router)
app.include_router(categories.router)
