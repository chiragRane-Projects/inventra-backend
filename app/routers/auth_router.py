from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.hash import hash_password, verify_password
from app.db.mongo import user_collection
from app.auth.jwt_handler import create_access_token, create_refresh_token
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.auth.deps import get_current_user

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"message": "Pong! Auth router is live  🎯"}

@router.post("/register")
def register(user: UserCreate):
    if user_collection.find_one({"username": user.username}):
        print("Username already exists!!\n")
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed = hash_password(user.password)
    new_user = {
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "password": hashed,
        "role": user.role
    }
    
    result = user_collection.insert_one(new_user)
    print("\nUser created successfully!!, \n", result)
    
    return{
        "message": "User created successfully",
        "id": str(result.inserted_id)
    }
    
@router.post("/login")
def login(user: UserLogin):
    db_user = user_collection.find_one({"username": user.username})
    if not db_user or not verify_password( user.password, db_user["password"]):
        print("Invalid Username or password\n")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token({"sub": db_user["username"]})
    refresh_token = create_refresh_token({"sub": db_user["username"]})
    
    print("\nUser logged-in!!, \n", access_token)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
@router.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user