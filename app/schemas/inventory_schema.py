from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class InventoryBase(BaseModel):
    name: str
    category: str
    quantity: float
    unit: str  
    price: float
    supplier: Optional[str] = None
    expiry_date: Optional[date] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    name: Optional[str]
    category: Optional[str]
    quantity: Optional[float]
    unit: Optional[str]
    price: Optional[float]
    supplier: Optional[str]
    expiry_date: Optional[date]

class InventoryResponse(InventoryBase):
    id: str
