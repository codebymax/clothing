from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header(...)):
    if x_token != "60241d51-db19-4f7f-b90c-05fcdf0ad714":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "maximillion":
        raise HTTPException(status_code=400, detail="No token provided")
