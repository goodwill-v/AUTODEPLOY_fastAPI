from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(
    title="FastAPI Template",
    description="Шаблонное FastAPI приложение.!!!!!МИНЗДРАВ ПРЕДУПРЕЖДАЕТ: ЛЕГКОМЫСЛЕННЫЕ КОММИТЫ УГРОЖАЮТ ЗДОРОВЬЮ",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Модели данных
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str = None
    price: float
    tax: float = None


# In-memory хранилище (в реальном приложении использовать БД)
items_db = []
next_id = 1


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "Добро пожаловать в FastAPI приложение!",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint для мониторинга"""
    return {"status": "healthy"}


@app.get("/items", response_model=List[ItemResponse])
async def get_items():
    """Получить все элементы"""
    return items_db


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Получить элемент по ID"""
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: Item):
    """Создать новый элемент"""
    global next_id
    new_item = {
        "id": next_id,
        **item.dict()
    }
    items_db.append(new_item)
    next_id += 1
    return new_item


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: Item):
    """Обновить элемент"""
    from fastapi import HTTPException
    index = next((i for i, it in enumerate(items_db) if it["id"] == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item = {
        "id": item_id,
        **item.model_dump()
    }
    items_db[index] = updated_item
    return updated_item


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """Удалить элемент"""
    from fastapi import HTTPException
    index = next((i for i, it in enumerate(items_db) if it["id"] == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_db.pop(index)
    return None


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
