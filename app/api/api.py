from fastapi import FastAPI
from .web_scraping.routes import router as web_scraping_router

def register_routes(app: FastAPI):
    app.include_router(web_scraping_router)