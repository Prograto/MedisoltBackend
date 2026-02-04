from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from jose import jwt
from app.config import JWT_SECRET

security = HTTPBearer()
ALGORITHM = "HS256"

def get_current_user(token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
