"""
Design out a children's book generation product.

Users
- Book
  - Book version
    - Pages
    - Images
    - Text
  - Page
    [
        {
            "image_url": "images.s3.com/1234",
            "x-position": "120",
            "y-position": "30",
            ...
        },
        {
            "text": "Once upon a time, there was a little rabbit.",
            "x-position": "120",
            "y-position": "30",
            ...
        }
    ]

books_table:
    - uuid
    - version
    - author_uuid

pages_table:
    - uuid
    - book_uuid
    - page_number
    - content_json


DATABASE SCALE
If we have 1M DAU - we'll be generating 1M books a day -> 400M books a year. 10 pages per book -> 4B pages per year.
    - Use a distributed database like DynamoDB
Access patterns:
    - User will load a book and update single pages often

"""

from typing import Optional

from data import bk_data
from repositories import bk_repo
from entities import bk_entity


def get_book(book_uuid: str, version: Optional[str] = None) -> bk_entity.Book:
    """Get book from DB by UUID"""
    book_repo = bk_repo.get_book_repo(bk_data.get_mock_db())
    bk = book_repo.rehydrate_book(book_uuid, version=version)

    return bk


if __name__ == "__main__":
    book_uuid = "book-uuid"
    version = "1.0"
    bk = get_book(book_uuid, version)
    print(bk)
