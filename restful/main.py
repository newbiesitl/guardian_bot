from fastapi import FastAPI
from pydantic import BaseModel
import json

class Item(BaseModel):
    name: str
    body: str = "{}"


app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    json_body = item.body
    j_load = json.loads(json_body)
    return j_load


