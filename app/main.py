from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.api import register_routes
from app.scheduler.keep_alive import keep_alive
from contextlib import asynccontextmanager
import asyncio

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(keep_alive())
    yield

app = FastAPI()
register_routes(app)