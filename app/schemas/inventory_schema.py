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
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    price: Optional[float] = None
    supplier: Optional[str] = None
    expiry_date: Optional[date] = None

class InventoryResponse(InventoryBase):
    id: str
