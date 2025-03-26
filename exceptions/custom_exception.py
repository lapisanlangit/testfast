import logging
from fastapi import HTTPException
import os
from models.response_model import ResponseModel
from typing import Any, List

# Konfigurasi logging
if os.getenv('ENVIRONTMENT') == 'development':
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",

        handlers=[
            logging.StreamHandler()                # Tampilkan log di konsol
        ]
    )
else:
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",

        handlers=[
            logging.FileHandler("app_errors.log"),  # Simpan log ke file
        ]
    )

logger = logging.getLogger(__name__)


class CustomException(HTTPException):
    def __init__(self, code: str, message: str, data: Any = None):
        if data is None:
            data = []
        self.response = ResponseModel(
            error="true",
            code=code,
            message=message,
            data=data
        )
        super().__init__(status_code=int(code), detail=self.response.dict())
