import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="My Basic Backend")

# CORS - allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str
    description: Optional[str] = None


# In-memory storage (restart par reset ho jayega)
items: dict[int, Item] = {}
counter = 0


@app.get("/")
def root():
    return {"message": "Backend is running on Railway!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items")
def list_items():
    return items


@app.post("/items")
def create_item(item: Item):
    global counter
    counter += 1
    items[counter] = item
    return {"id": counter, "item": item}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"deleted": item_id}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
