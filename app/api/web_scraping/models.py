from pydantic import BaseModel
from typing import List, Optional

class getData(BaseModel):
    titulo: str
    url: str
    imagem: str
    lide: Optional[str] = None    
    fonte: str

class getResponse(BaseModel):
    total_count: int
    data: List[getData]