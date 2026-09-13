from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database  import init_db
from .routes.auth import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)

@app.get('/health')
def health():
    return {"status": "ok"}