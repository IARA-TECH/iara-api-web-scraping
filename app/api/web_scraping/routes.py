from fastapi import APIRouter

from .models import getResponse
from . import usecases

router = APIRouter(prefix='/news', tags=['Web Scraping'])

@router.get('', response_model=getResponse)
def get() -> getResponse:
    news = usecases.get()
    return {'total_count': len(news), 'data': news}