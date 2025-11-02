from fastapi import FastAPI
from .web_scraping.routes import router as web_scraping_router
from app.scheduler.routes.health import router as health_router

def register_routes(app: FastAPI):
    app.include_router(web_scraping_router)
    app.include_router(health_router)