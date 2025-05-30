from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.auth.deps import require_staff, require_admin
from app.schemas.inventory_schema import InventoryCreate, InventoryResponse, InventoryUpdate
from app.db.mongo import inventory_collection
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/", response_model=InventoryResponse)
def create_item(item: InventoryCreate, user=Depends(require_staff)):
    item_dict = item.model_dump()

    if item_dict.get("expiry_date"):
        item_dict["expiry_date"] = datetime.combine(item_dict["expiry_date"], datetime.min.time())

    res = inventory_collection.insert_one(item_dict)
    item_dict["id"] = str(res.inserted_id)
    return item_dict