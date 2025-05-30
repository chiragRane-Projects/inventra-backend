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

@router.get("/", response_model=List[InventoryResponse])
def get_all_items(user=Depends(require_staff)):
    items = []
    for item in inventory_collection.find():
        item["id"] = str(item["_id"])
        items.append(item)
    return items

@router.get("/{id}", response_model=InventoryResponse)
def get_item(id:str, user=Depends(require_staff)):
    item = inventory_collection.find_one({"_id": ObjectId(id)})
    if not item:
        print("No items found!!")
        raise HTTPException(status_code=404, detail="Item not found")
    item['id'] = str(item['_id'])
    return item

@router.put("/{id}", response_model=InventoryResponse)
def update_item(id: str, update: InventoryUpdate, user=Depends(require_staff)):
    update_dict = {k: v for k, v in update.dict().items() if v is not None}
    result = inventory_collection.update_one({"_id": ObjectId(id)}, {"$set": update_dict})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item = inventory_collection.find_one({"_id": ObjectId(id)})
    item["id"] = str(item["_id"])
    return item

@router.delete("/{id}")
def delete_item(id: str, user=Depends(require_admin)):
    result = inventory_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}    