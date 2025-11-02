from fastapi import HTTPException


class InternalServerError(HTTPException):
    def __init__(self, action: str = None):
        message = f"Erro interno ao {action}" if action else "Erro interno"
        super().__init__(status_code=500, detail=message)
