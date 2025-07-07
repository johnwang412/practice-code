from fastapi import FastAPI
from fastapi.responses import JSONResponse

from logic import shorten_url


app = FastAPI()


@app.get("/health")
def health():
    shorten_url._sanitize('')
    return JSONResponse(content={"status": "ok"})
