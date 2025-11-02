from dotenv import load_dotenv
from fastapi import FastAPI

from .api.api import register_routes

load_dotenv()

app = FastAPI()
register_routes(app)