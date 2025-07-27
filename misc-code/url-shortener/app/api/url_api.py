from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from database import get_db
from logic.shorten_url import create_short_url, get_original_url


app = FastAPI(title="URL Shortener Service", version="1.0.0")

# You can see thread pool info in logs by adding this startup event
@app.on_event("startup")
async def startup_event():
    import asyncio
    loop = asyncio.get_event_loop()
    print(f"Thread pool executor: {loop._default_executor}")
    print(f"Max workers: {loop._default_executor._max_workers if loop._default_executor else 'Default'}")


class URLRequest(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    original_url: str
    short_code: str
    short_url: str


@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"})


@app.put("/shorten", response_model=URLResponse)
def shorten_url_endpoint(
    request: URLRequest,
    db: Session = Depends(get_db)
):
    """
    Create a short URL for the given original URL.

    Args:
        request: URLRequest containing the URL to shorten
        db: Database session

    Returns:
        URLResponse with original URL, short code, and full short URL
    """
    return URLResponse(
        original_url=str(request.url),
        short_code='foo',
        short_url='http://foo.bar/baz',
    )


    url_mapping = create_short_url(str(request.url), db)

    if not url_mapping:
        raise HTTPException(
            status_code=500,
            detail="Failed to create short URL. Please try again."
        )

    # In a real deployment, this would be your actual domain
    base_url = "http://localhost:8000"
    short_url = f"{base_url}/{url_mapping.short_code}"

    return URLResponse(
        original_url=url_mapping.original_url,
        short_code=url_mapping.short_code,
        short_url=short_url
    )


@app.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    """
    Redirect to the original URL for the given short code.

    Args:
        short_code: The short code to look up
        db: Database session

    Returns:
        RedirectResponse to the original URL
    """
    original_url = get_original_url(short_code, db)

    if not original_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return RedirectResponse(url=original_url, status_code=301)
