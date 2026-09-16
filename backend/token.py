import jwt
from datetime import datetime, timedelta, timezone
import os

def create_access_token(user_id):
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    secret_key = os.getenv("SECRET_KEY")

    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token