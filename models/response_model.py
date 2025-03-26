from typing import Any, List
from pydantic import BaseModel


class ResponseModel(BaseModel):
    error: str  # "true" atau "false"
    code: str   # Kode status sebagai string
    message: str  # Pesan sukses atau error
    data: Any  # Data yang dikembalikan (bisa array, objek, dll.)

    class Config:
        schema_extra = {
            "example": {
                "error": "false",
                "code": "200",
                "message": "get data success sekali",
                "data": []
            }
        }
