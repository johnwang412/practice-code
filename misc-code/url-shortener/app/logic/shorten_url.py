import hashlib
import secrets
import string
from typing import Optional
from sqlalchemy.orm import Session
from bos.url_repository import URLRepository
from models import URLMapping


def _sanitize(url: str) -> str:
    """
    Sanitizes the URL by removing any leading or trailing whitespace and
    converting it to lowercase.
    """
    return url.strip().lower()


def _generate_short_code(url: str, length: int = 8) -> str:
    """
    Generate a short code for the given URL.
    First tries a hash-based approach, then falls back to random generation.
    """
    # Try hash-based approach first for consistency
    sanitized_url = _sanitize(url)
    url_hash = hashlib.md5(sanitized_url.encode()).hexdigest()[:length]
    return url_hash


def _generate_random_short_code(length: int = 8) -> str:
    """
    Generate a random short code using alphanumeric characters.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def create_short_url(url: str, db: Session) -> Optional[URLMapping]:
    """
    Create a short URL mapping and store it in the database.

    Args:
        url: The original URL to shorten
        db: Database session

    Returns:
        URLMapping object if successful, None if failed
    """
    if not url or not url.strip():
        return None

    sanitized_url = _sanitize(url)
    repository = URLRepository(db)

    # Check if URL already exists
    existing_mapping = repository.get_url_by_original_url(sanitized_url)
    if existing_mapping:
        return existing_mapping

    # Generate short code
    short_code = _generate_short_code(sanitized_url)

    # If hash-based code already exists, try random codes
    max_attempts = 10
    attempt = 0
    while repository.short_code_exists(short_code) and attempt < max_attempts:
        short_code = _generate_random_short_code()
        attempt += 1

    if attempt >= max_attempts:
        return None  # Failed to generate unique code

    # Create the mapping
    return repository.create_url_mapping(sanitized_url, short_code)


def get_original_url(short_code: str, db: Session) -> Optional[str]:
    """
    Retrieve the original URL for a given short code.

    Args:
        short_code: The short code to look up
        db: Database session

    Returns:
        Original URL if found, None otherwise
    """
    if not short_code or not short_code.strip():
        return None

    repository = URLRepository(db)
    mapping = repository.get_url_by_short_code(short_code.strip())
    return mapping.original_url if mapping else None


# Legacy function for backward compatibility
def shorten_url(url: str) -> str:
    """
    Legacy function that generates a short code without database storage.
    This is kept for backward compatibility with existing code.
    """
    return _generate_short_code(url)