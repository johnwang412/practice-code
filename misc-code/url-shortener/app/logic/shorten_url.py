import hashlib


def _sanitize(url: str) -> str:
    """
    Sanitizes the URL by removing any leading or trailing whitespace and
    converting it to lowercase.
    """
    return url.strip().lower()


def shorten_url(url: str) -> str:
    """
    Shortens a given URL using a simple hash function.
    """
    # Sanitize the URL
    sanitized_url = _sanitize(url)

    # Create a hash of the URL
    url_hash = hashlib.md5(sanitized_url.encode()).hexdigest()[:8]

    # Return the shortened URL
    return url_hash