import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db

async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    now = datetime.utcnow()
    data_with_meta = {**data, "created_at": now, "updated_at": now}
    result = await db[collection_name].insert_one(data_with_meta)
    created = await db[collection_name].find_one({"_id": result.inserted_id})
    if created and "_id" in created:
        created["id"] = str(created.pop("_id"))
    return created or {}

async def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    db = await get_db()
    filter_dict = filter_dict or {}
    cursor = db[collection_name].find(filter_dict).limit(limit)
    items: List[Dict[str, Any]] = []
    async for doc in cursor:
        if "_id" in doc:
            doc["id"] = str(doc.pop("_id"))
        items.append(doc)
    return items
