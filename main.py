from fastapi import FastAPI, Request
from routes.item_route import router as item_router
import time
import logging

from datetime import datetime
import json

app = FastAPI()

# Middleware untuk logging permintaan


@app.middleware("http")
async def log_request_data(request: Request, call_next):
    method = request.method
    url = str(request.url)
    query_params = dict(request.query_params)

    # Untuk membaca body, kita perlu 'stream' ulang karena hanya bisa dibaca sekali
    body_bytes = await request.body()
    try:
        body = body_bytes.decode('utf-8')
        body_data = json.loads(body) if body else {}
    except Exception:
        body_data = body  # Bisa saja bukan JSON (misal: form)

    now = datetime.now()
    print("------ Incoming Request ------")
    print(f"Time       : {now}")
    print(f"Method     : {method}")
    print(f"URL        : {url}")
    print(f"Query      : {query_params}")
    print(f"Body       : {body_data}")
    print("-----------------------------")

    # Buat ulang request dengan body agar bisa diteruskan
    request = Request(request.scope, receive=lambda: {
                      'type': 'http.request', 'body': body_bytes})

    response = await call_next(request)
    return response

# Register routes
app.include_router(item_router, prefix="/items", tags=["Items"])


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}
