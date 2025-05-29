from fastapi import APIRouter, Depends
from app.auth.deps import require_admin, require_staff

router = APIRouter()

@router.get("/admin-data", dependencies=[Depends(require_admin)])
async def admin_data():
    return {"secret": "only for admins"}

@router.get("/staff-data", dependencies=[Depends(require_staff)])
async def staff_data():
    return {"Staff data"}