from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt_handler import decode_token
from app.db.mongo import user_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    
    payload = decode_token(token)
    print("DECODED PAYLOAD:", payload)
    if payload is None or "sub" not in payload:
        raise credentials_exception
    
    username = payload['sub']
    user = user_collection.find_one({"username": username})
    
    if not user:
        raise credentials_exception
    
    return{
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"]
    }
    
def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

def require_staff(user: dict = Depends(get_current_user)):
    if user["role"] not in ["admin", "staff"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff access required"
        )
    return user
