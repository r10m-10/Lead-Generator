import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import get_db
from .models.user import User
import os

security_scheme = HTTPBearer()

def create_access_token(user_id):
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    secret_key = os.getenv("SECRET_KEY")

    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token

def decode_token(access_token):
    secret_key = os.getenv("SECRET_KEY")
    payload = jwt.decode(access_token, secret_key, algorithms=["HS256"])
    return payload

def get_current_user(credentials = Depends(security_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials

    try:
        user_id = decode_token(token)["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=e)

    query = select(User).where(User.id == user_id)
    user = db.execute(query).scalar_one_or_none()

    if user is None:
        raise HTTPException (status_code=400, detail="User does not exist")

    return user

